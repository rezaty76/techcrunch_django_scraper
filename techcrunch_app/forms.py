from django import forms
from techcrunch_app import scraper_config


class DailySearchForm(forms.Form):
    """
    Form for daily search functionality.
    """

    dummy = forms.CharField(widget=forms.HiddenInput(), initial='dummy')  # A hidden field for form submission


class SearchByKeywordForm(forms.Form):
    """
    Form for searching articles by keyword.
    """

    keyword = forms.CharField(
        label='Keyword',
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'input--style-1',  # CSS class for styling
                                      'placeholder': 'Keyword to search for . . .',  # Placeholder text
                                      'type': 'text',  # Input type
                                      'required': True,  # Required field
                                      'label_attrs': {'class': 'label'}})  # CSS class for label
    )
    max_pages = forms.IntegerField(
        label='Page Count',
        min_value=scraper_config.MINIMUM_SEARCH_PAGE_COUNT,  # Minimum allowed page count
        max_value=scraper_config.MAXIMUM_SEARCH_PAGE_COUNT,  # Maximum allowed page count
        widget=forms.NumberInput(attrs={'class': 'input--style-1',  # CSS class for styling
                                        'placeholder': 'Number of pages to search for . . .',  # Placeholder text
                                        'type': 'number',  # Input type
                                        'required': True,  # Required field
                                        'label_attrs': {'class': 'label'}})  # CSS class for label
    )
