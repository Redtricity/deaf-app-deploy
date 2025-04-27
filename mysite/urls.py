"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views
from django.urls import include
from .views import mycommunity
from django.conf import settings
from django.conf.urls.static import static
from .views import create_community
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('explore/', views.explore, name='explore'), 
    path('', RedirectView.as_view(url='/accounts/login', permanent=True)),  # Redirect root to login
    path('mycommunity/', views.mycommunity, name='mycommunity'),
    path('events/', views.events, name= 'events' ),
    path('create-community/', create_community, name='create_community'),
    path('community/<int:community_id>/toggle-membership/', views.toggle_community_membership, name='toggle_community_membership'),
    path('community/<int:community_id>/', views.community_detail, name='community_detail'),
    path('community/delete/<int:community_id>/', views.delete_community, name='delete_community'),
    path('like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
