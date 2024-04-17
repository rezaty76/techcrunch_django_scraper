from django.contrib import admin
from django.contrib.admin import register
from import_export.admin import ImportExportModelAdmin
from techcrunch_app.models import (Url,
                                   Category,
                                   Author,
                                   Article,
                                   Keyword,
                                   SearchByKeyword,
                                   ArticleSearchByKeywordItem,
                                   )


class BaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Base admin class providing common functionalities for other admin classes.
    """

    actions = ('activate', 'deactivate')  # Define custom actions for bulk updating
    search_fields = ['title']  # Enable search functionality on the specified fields

    @admin.action
    def activate(self, request, queryset):
        """
        Custom admin action to activate selected objects.
        """
        queryset.update(is_active=True)

    @admin.action
    def deactivate(self, request, queryset):
        """
        Custom admin action to deactivate selected objects.
        """
        queryset.update(is_active=False)


@register(Article)
class ArticleAdmin(BaseAdmin):
    """
    Admin class for the Article model.
    """

    list_display = ['id',
                    'site_id',
                    'title',
                    'category',
                    'author',
                    'description',
                    'is_active',
                    'created_at',
                    'updated_at']

    list_filter = ['slug',
                   'category',
                   'author',
                   'is_active',
                   'created_at',
                   'updated_at',
                   ]
    list_display_links = ['id', 'site_id', 'title']  # Make specified fields clickable in the list view
    search_fields = ['title', 'slug', 'site_id', 'author_position']  # Enable search functionality


@register(Category)
class CategoryAdmin(BaseAdmin):
    """
    Admin class for the Category model.
    """

    list_display = ['id',
                    'site_id',
                    'title',
                    'is_active',
                    'created_at',
                    'updated_at',
                    ]

    search_fields = ['title', 'slug', 'site_id']
    list_filter = ['title', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'site_id', 'title']


@register(Author)
class AuthorAdmin(BaseAdmin):
    """
    Admin class for the Author model.
    """

    list_display = ['id',
                    'site_id',
                    'title',
                    'author_position',
                    'is_active',
                    'created_at',
                    'updated_at',
                    ]

    search_fields = ['title', 'slug', 'site_id', 'author_position']
    list_filter = ['author_position', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'site_id', 'title']


@register(Keyword)
class KeywordAdmin(BaseAdmin):
    """
    Admin class for the Keyword model.
    """

    list_display = ['id', 'slug', 'times_searched']
    list_display_links = ['id', 'slug']
    list_filter = []


@register(SearchByKeyword)
class SearchByKeywordAdmin(BaseAdmin):
    """
    Admin class for the SearchByKeyword model.
    """

    list_display = ['keyword',
                    'max_pages',
                    'is_active',
                    'search_at',
                    'new_articles',
                    'scrapped_articles',
                    ]
    list_display_links = ['keyword']
    list_filter = ['search_at', 'is_active']
    search_fields = ['keyword']


@register(ArticleSearchByKeywordItem)
class ArticleSearchByKeywordItemAdmin(BaseAdmin):
    """
    Admin class for the ArticleSearchByKeywordItem model.
    """

    list_display = ['search_by_keyword', 'article', 'is_scrapped']
    list_display_links = ['search_by_keyword']
    list_filter = ['search_by_keyword', 'is_scrapped']
    search_fields = ['search_by_keyword']


@register(Url)
class UrlAdmin(admin.ModelAdmin):
    """
    Admin class for the Url model.
    """

    list_display = ['id', 'address', 'created_at']
    list_display_links = ['id', 'address']
    list_filter = ['created_at']
    search_fields = ['address']


class ArticleCategoryAdmin(BaseAdmin):
    """
    Admin class for the ArticleCategory model.
    """

    list_display = ('title', 'category_order',)
    list_filter = ('category',)
