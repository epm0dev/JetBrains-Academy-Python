from json import load, dump
from typing import Dict
from django.forms import forms, fields
from django.shortcuts import render
from django.views import View
from django.conf import settings
from datetime import datetime
from django.shortcuts import redirect


# Read the JSON array of news articles from the application's NEWS_JSON_PATH.
def read_articles():
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        articles = load(json_file)
    return articles


# Read the JSON array of news articles from the application's NEWS_JSON_PATH, append the specified article, and dump the
# updated JSON array back to the same JSON file.
def append_article(article: Dict):
    articles = read_articles()
    articles.append(article)
    with open(settings.NEWS_JSON_PATH, 'w+') as json_file:
        dump(articles, json_file)


# A search form to be displayed in the main view, allowing the user to search for news articles by title.
class SearchForm(forms.Form):
    # The form has a single CharField for the user to input a string to search for in the titles of the news articles.
    q = fields.CharField(label='Search:', min_length=1, max_length=100, strip=True)


# Displays a list of all of the news articles, grouped by date, and sorted from newest to oldest.
class MainView(View):
    # Handle GET requests.
    @staticmethod
    def get(request):
        # Create an instance of the SearchForm class.
        form = SearchForm(request.GET, initial={'q': ''})

        if form.is_valid():
            # If the form is valid, retrieve the user's query and populate a new list with news articles whose titles
            # contain the that query.
            query = form.cleaned_data['q']
            matches = []
            for article in read_articles():
                if query in article['title']:
                    matches.append(article)

            # Create a context dictionary to populate the search.html template when rendered.
            context = {'articles': matches}

            # Return an HttpResponse object containing the rendered template.
            return render(
                request, 'news/search.html', context
            )
        else:
            # If the form is invalid, create a context dictionary to populate the main.html template when rendered.
            context = {'articles': read_articles(), 'form': SearchForm(request.GET)}

            # Return an HttpResponse object containing the rendered template.
            return render(
                request, 'news/main.html', context
            )


# Displays the contents of a single news article.
class ArticleView(View):
    # Handle GET requests.
    @staticmethod
    def get(request, article_link):
        # Iterate through all of the news articles until one is found whose link matches the link from the url.
        for article in read_articles():
            if int(article['link']) == int(article_link):
                # Create a context dictionary to populate the article.html template when rendered.
                context = {'article': article}

                # Return an HttpResponse object containing the rendered template.
                return render(
                    request, 'news/article.html', context
                )

        # If no matching news article was found, redirect the user back to the main news page.
        return redirect('/news/')


# Displays a form allowing the user to create a new news article.
class CreateView(View):
    # Handle GET requests.
    @staticmethod
    def get(request):
        # Return an HttpResponse object containing the rendered create.html template.
        return render(
            request, 'news/create.html'
        )

    # Handle POST requests.
    @staticmethod
    def post(request):
        # Store a datetime object of the current time and date.
        now = datetime.now()

        # Generate and store the values of the new news article's fields.
        created = now.strftime('%Y-%m-%d %H:%M:%S')
        text = request.POST.get('text')
        title = request.POST.get('title')
        link = int(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}')

        # Append a dictionary containing the values stored above and append it to the current JSON array of articles.
        append_article({'created': created, 'text': text, 'title': title, 'link': link})

        # Redirect the user back to the main news page.
        return redirect('/news/')
