from django.urls import path
from django.conf.urls import url
from ucamwebauth.views import raven_login, raven_logout, raven_return

from . import views

urlpatterns = [
    path('availabilities/', views.availabilities, name='availabilities'),
    path('', views.UserOutingMemberListView.as_view(), name='outings'),
    path('<uuid:pk>/', views.UserOutingDetailView.as_view(), name='outing-detail'),
    path('group-availabilities/', views.CombinedAvailabilityView.as_view(), name='group-availabilities'),
    path('create/', views.create_outing, name='create'),
    path('<uuid:pk>/update/', views.create_outing, name='update'),
]