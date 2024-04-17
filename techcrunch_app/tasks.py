from . import scraper_config
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from .scraper_handler import ScrapperHandler
from .models import SearchByKeyword, Keyword, Author, Category

models = {'author': Author,
          'category': Category,
          'keyword': Keyword}


@shared_task()
def search_by_keyword_task(user_name, keyword, max_page=scraper_config.SEARCH_PAGE_COUNT):
    """
    Celery task for searching articles by keyword.

    Args:
        user_name (str): The username of the user initiating the search.
        keyword (str): The keyword to search for.
        max_page (int): The maximum number of pages to search (default is set in scraper_config).

    Returns:
        dict: A dictionary containing information about the search task.
    """
    User = get_user_model()
    current_user = User.objects.get(username=user_name)
    print(f'search_by_keyword_task => {keyword} - pages({max_page}) by user ({current_user}) Started')
    keyword, _ = Keyword.objects.get_or_create(
        slug=keyword,
    )
    keyword.times_searched += 1
    keyword.save()

    scraper_handler = ScrapperHandler()

    search_by_keyword = SearchByKeyword.objects.create(
        user=current_user,
        keyword=keyword,
        max_pages=max_page
    )
    scraped_item_count = scraper_handler.manual_search_method(search_by_keyword_instance=search_by_keyword)

    print(
        f'search_by_keyword_task => {keyword} - pages({search_by_keyword.max_pages}) by user ({current_user}) finished')

    return {
        'keyword': keyword.slug,
        'max_page': max_page,
        'scraped_item_count': scraped_item_count,
        'status': 'finished',
    }


@shared_task()
def daily_search_task():
    """
    Celery task for performing daily scraping of articles, authors, and categories.
    """
    print(f'daily_scrape_task => by (Automation)  Started')
    scraper_handler = ScrapperHandler()
    scraper_handler.daily_scrape()
    print(f'daily_search_task => by (Automation) finished')
