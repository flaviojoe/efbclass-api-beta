# -*- coding: utf-8 -*-

from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home')),
    path('home', views.IndexView.as_view(), name='home'),
]
