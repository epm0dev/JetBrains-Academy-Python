"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from .views import MySignupView, MyLoginView, ProfileView
from menu.views import MenuView
from resume.views import ResumeListView, NewResumeView
from vacancy.views import VacancyListView, NewVacancyView


# Route supported URLs to their corresponding handlers.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MenuView.as_view()),
    path('home', ProfileView.as_view()),
    path('resumes', ResumeListView.as_view()),
    path('resume/new', NewResumeView.as_view()),
    path('vacancies', VacancyListView.as_view()),
    path('vacancy/new', NewVacancyView.as_view()),
    path('login', MyLoginView.as_view()),
    path('signup', MySignupView.as_view()),
    path('home/', RedirectView.as_view(url='/home')),
    path('resumes/', RedirectView.as_view(url='/resumes')),
    path('resume/new/', RedirectView.as_view(url='/resume/new')),
    path('vacancies/', RedirectView.as_view(url='/vacancies')),
    path('vacancy/new/', RedirectView.as_view(url='/vacancy/new')),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
]
