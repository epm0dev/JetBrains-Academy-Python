from django.urls import path, re_path
from .views import MainView, ArticleView, CreateView


# Route supported URLs to their corresponding view classes.
urlpatterns = [
    path('', MainView.as_view()),
    path('create/', CreateView.as_view()),
    re_path("(?P<article_link>[^/]*)/?", ArticleView.as_view()),
]
