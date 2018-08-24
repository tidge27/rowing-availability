from django.urls import path
from django.conf.urls import url
from ucamwebauth.views import raven_login, raven_logout, raven_return

from . import views

urlpatterns = [
    path('users/', views.index, name='index'),
    url('login/raven/', raven_login, name='raven_login'),
    url('logout/raven/', raven_logout, name='raven_logout'),
    url('raven_return/', raven_return, name='raven_return'),
]