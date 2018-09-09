from django.urls import path
from django.conf.urls import url
from ucamwebauth.views import raven_login, raven_logout, raven_return

from . import views

urlpatterns = [
    path('availabilities', views.availabilities, name='availabilities'),
    path('outings', views.UserOutingMemberListView.as_view(), name='outings'),
    path('outing/<uuid:pk>', views.UserOutingDetailView.as_view(), name='outing-detail'),
    path('group-availabilities', views.CombinedAvailabilityView.as_view(), name='group-availabilities'),
]