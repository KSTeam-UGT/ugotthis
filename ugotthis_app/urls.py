from django.contrib import admin
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('users/<username>/', views.user_page, name="user_page"),
    path('register/', views.registration, name="registration"),
    path('logout/', views.logout_user, name="logout_user"),
    # path('profile/', views.profile_page),
]
