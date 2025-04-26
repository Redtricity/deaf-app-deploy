from django.urls import path
from . import views
from django.urls import include
from .views import profile_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('editprofile/', views.edit_profile_view, name='editprofile'),
    path('search/', views.search_profiles, name='search_profiles'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('revoke_follow_request/<str:username>/', views.revoke_follow_request, name='revoke_follow_request'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('profile/<username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<username>/following/', views.following_list, name='following_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/accept/<int:notification_id>/', views.accept_follow_request, name='accept_follow_request'),
    path('notifications/reject/<int:notification_id>/', views.reject_follow_request, name='reject_follow_request'),
]