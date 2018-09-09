from django.urls import path
from django.conf.urls import url
from ucamwebauth.views import raven_login, raven_logout, raven_return

from . import views

urlpatterns = [
    path('groups', views.GroupListView.as_view(), name='groups'),
    path('create', views.create_group, name='create'),
    # path('group/<uuid:pk>', views.UserOutingDetailView.as_view(), name='outing-detail'),
]