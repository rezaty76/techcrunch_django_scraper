from django.contrib.auth import get_user_model
from django.db import models
from bs4 import BeautifulSoup as Bs
import requests
from techcrunch_app.scraper_config import SEARCH_PAGE_COUNT

User = get_user_model()


class ItemsBaseModel(models.Model):
    """
    Base model for common fields used across different item types.
    """

    site_id = models.CharField(max_length=200, verbose_name='site_id', db_index=True)
    slug = models.CharField(max_length=500, verbose_name='slug', null=True, blank=True)
    title = models.CharField(max_length=500, verbose_name='title', null=True, blank=True)
    url = models.URLField(verbose_name='URL', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='is_active', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_date', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Untitled"


class Url(models.Model):
    """
    Model to store URLs and their corresponding status codes.
    """

    address = models.CharField(max_length=500, verbose_name='URL_address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    status_code = models.IntegerField(verbose_name='status_code', null=True, blank=True, default=0)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def get_response(self):
        """
        Sends a request to the URL and retrieves the response object.
        """

        response = requests.get(url=self.address, allow_redirects=False)
        self.status_code = response.status_code
        if self.status_code != 200 and self.status_code != 201:
            print(f"Send request to ({self.address}) - Response code: {self.status_code}")
            response = None
        else:
            print(f"Send request to ({self.address}) - Response code: {self.status_code}")
        return response

    def get_json(self):
        """
        Retrieves JSON data from the URL response.
        """

        res = self.get_response()
        if res is not None:
            return res.json()
        else:
            return None

    def get_any_soup(self):
        """
        Retrieves BeautifulSoup object from the HTML content of the URL response.
        """

        res = self.get_response()
        if res is not None:
            soup = Bs(res.text, 'html.parser')
            return soup
        else:
            return None


class Category(ItemsBaseModel):
    """
    Model to represent categories of articles.
    """

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Author(ItemsBaseModel):
    """
    Model to represent authors of articles.
    """

    author_position = models.CharField(max_length=200, verbose_name='author_position', null=True, blank=True)
    author_avatars = models.CharField(max_length=500, verbose_name='author_avatars_links', null=True, blank=True)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'


class Article(ItemsBaseModel):
    """
    Model to represent articles.

    Inherits:
        ItemsBaseModel: Base model for items.

    Attributes:
        category (ForeignKey): The category to which the article belongs.
        author (ForeignKey): The author of the article.
        image (CharField): The URL or path to the image associated with the article.
        description (TextField): The description or content of the article.
    """

    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.TextField(verbose_name='description', null=True, blank=True)

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'


class ArticleCategory(models.Model):
    """
    Model to represent the relationship between articles and categories.
    """

    category_order = models.IntegerField(default=0)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_categories"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="article_categories"
    )

    class Meta:
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return f"{self.article.title} - {self.category.title}"


class Keyword(models.Model):
    """
    Model to represent keywords.
    """

    slug = models.CharField(max_length=500, verbose_name='slug')
    times_searched = models.IntegerField(verbose_name='searching_times', default=0, null=True, blank=True)

    class Meta:
        verbose_name = 'keyword'
        verbose_name_plural = 'keywords'

    def __str__(self):
        return self.slug


class SearchByKeyword(models.Model):
    """
    Model to store search requests made by users based on keywords.
    """

    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE, null=True, blank=True)
    keyword = models.ForeignKey(
        Keyword,
        verbose_name='keyword',
        on_delete=models.CASCADE,
        related_name='search_by_keyword'
    )
    max_pages = models.IntegerField(verbose_name='max_pages', null=True, blank=True, default=SEARCH_PAGE_COUNT)

    new_articles = models.IntegerField(verbose_name='new_articles', null=True, blank=True, default=0)
    scrapped_articles = models.TextField(verbose_name='scrapped_articles', null=True, blank=True, default="Nothing")

    search_at = models.DateField(verbose_name='search_at', auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)

    class Meta:
        verbose_name = 'search_by_keyword'
        verbose_name_plural = 'search_by_keywords'

    def __str__(self):
        return self.keyword.__str__()

    def result_message(self):
        first_string_to_log = f'Searching Result for keyword ({self.keyword}) in date ({self.search_at})'
        second_string_to_log = f'{self.scrapped_articles}'
        print(first_string_to_log)
        print(second_string_to_log)


class ArticleSearchByKeywordItem(models.Model):
    """
    Model to represent articles found through keyword-based search requests.
    """

    search_by_keyword = models.ForeignKey(
        SearchByKeyword,
        related_name='article_search_by_keyword_items',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        related_name='article_search_by_keyword_items',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='article_searched_by_keyword'
    )
    is_scrapped = models.BooleanField(verbose_name='is_scrapped', default=True)

    class Meta:
        verbose_name = 'Articles Search By Keyword Item'
        verbose_name_plural = 'Articles Search By Keyword Items'

    def __str__(self):
        return f'({self.search_by_keyword.keyword.slug})'


class DailyUpdateData(models.Model):
    """
    Model to store daily updates of article, category, and author data.
    """

    article_items = models.TextField(verbose_name='New_Articles', null=True, blank=True, default='nothing')
    category_items = models.TextField(verbose_name='New_Category', null=True, blank=True, default='nothing')
    author_items = models.TextField(verbose_name='New_Author', null=True, blank=True, default='nothing')
    search_date = models.DateTimeField(verbose_name='scrapped_date')
    is_active = models.BooleanField(default=True, verbose_name='is_active', null=True, blank=True)

    class Meta:
        verbose_name = 'Daily Update Data'
        verbose_name_plural = 'Daily Update Data'

    def __str__(self):
        return f'Updated Data at :({self.search_date})'
