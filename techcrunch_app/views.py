from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib
import base64
from techcrunch_app.forms import SearchByKeywordForm, DailySearchForm
from techcrunch_app.tasks import search_by_keyword_task, daily_search_task
from .models import Category, ArticleCategory


@login_required
def dayli_search_view(request):
    """
    View function for performing daily search task.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the homepage after processing the task.
        HttpResponse: Renders the daily search form on GET request.
    """
    if request.method == 'POST':
        # If the form is submitted, process the task and redirect to the homepage
        daily_search_task.delay()  # Assuming daily_search_task is a Celery task
        return redirect('search')  # Redirect to the homepage or any other desired URL
    else:
        # If it's a GET request, create an instance of the form and render the template
        form = DailySearchForm()
    return render(request, 'techcrunch/dayli_search.html', {'form': form})


def charts_view(request, model_name):
    """
    View function for rendering charts based on model data.

    Args:
        request (HttpRequest): The HTTP request object.
        model_name (str): The name of the model for which charts are generated.

    Returns:
        HttpResponse: Renders the chart template.
    """
    categories = Category.objects.all()
    categories_name = []
    categories_count = []

    for category in categories:
        categories_name.append(category.title)  # Assuming 'title' represents the name of the category
        article_count = ArticleCategory.objects.filter(category=category).count()
        categories_count.append(article_count)

    # Configure Matplotlib to use a non-interactive backend
    plt.switch_backend('agg')

    plt.bar(categories_name, categories_count)
    fig = plt.gcf()

    # Convert the graph into a string buffer and then encode it as a base64 string
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()

    # Create a data URI for the image
    uri = urllib.parse.quote(string)

    return render(request, 'techcrunch/charts.html', {'data': uri})


@login_required
def search_view(request):
    """
    View function for searching articles by keyword.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the search form template.
    """
    current_user_user_name = request.user.username
    if request.method == 'POST':
        form = SearchByKeywordForm(request.POST)
        if form.is_valid():
            result = search_by_keyword_task.delay(
                user_name=current_user_user_name,
                keyword=form.cleaned_data['keyword'],
                max_page=form.cleaned_data['max_pages'],
            )
            print(f'techcrunch_search_by_keyword_task:({result})', )
    else:
        form = SearchByKeywordForm()

    return render(request, 'techcrunch/search.html', {'form': form})
