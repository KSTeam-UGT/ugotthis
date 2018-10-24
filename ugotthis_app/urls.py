from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('users/<username>/', views.user_page, name="user_page"),
    path('users/<username>/', views.user_page, name="user_page"),
    path('register/', views.registration, name="registration"),
    path('logout/', views.logout_user, name="logout_user"),
    # path('profile/', views.profile_page, name="profile_page"),
    # path('user-content/', views.user_content, name="user_content"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
