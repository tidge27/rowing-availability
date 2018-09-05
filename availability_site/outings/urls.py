from django.urls import path
from django.conf.urls import url
from ucamwebauth.views import raven_login, raven_logout, raven_return

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]