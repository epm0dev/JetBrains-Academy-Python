"""hypercar URL Configuration

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
from django.urls import path
from django.views.generic import RedirectView
from tickets.views import WelcomeView, MenuView, TicketView, OperatorView, NextView


# Route supported URLs to their corresponding view classes.
urlpatterns = [
    path('welcome/', RedirectView.as_view(url='/welcome')),
    path('welcome', WelcomeView.as_view()),
    path('menu/', RedirectView.as_view(url='/menu')),
    path('menu', MenuView.as_view()),
    path('get_ticket/change_oil/', RedirectView.as_view(url='/get_ticket/change_oil')),
    path('get_ticket/change_oil', TicketView.as_view()),
    path('get_ticket/inflate_tires/', RedirectView.as_view(url='/get_ticket/inflate_tires')),
    path('get_ticket/inflate_tires', TicketView.as_view()),
    path('get_ticket/diagnostic/', RedirectView.as_view(url='/get_ticket/diagnostic')),
    path('get_ticket/diagnostic', TicketView.as_view()),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('processing', OperatorView.as_view()),
    path('next/', RedirectView.as_view(url='/next')),
    path('next', NextView.as_view()),
    path('', WelcomeView.as_view())
]
