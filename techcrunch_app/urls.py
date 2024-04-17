from django.urls import path
from .views import search_view, dayli_search_view, charts_view

urlpatterns = [
    path('dayli_search/', dayli_search_view, name='dayli_search'),
    path('', search_view, name='search'),
    path('charts/<slug:model_name>', charts_view, name='charts'),
]
