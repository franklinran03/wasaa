"""
URL configuration for wasaa project.

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
from django.urls import path
from social import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


handler404 = 'social.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_post/', views.create_post, name='create_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('myprofile/<str:username>', views.my_profile, name='my_profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', views.delete_user, name='delete_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/post/<int:post_id>/edit/', views.edit_post, name='edit_post'),

    path('post/<int:post_id>/delete_image/', views.delete_post_image, name='delete_post_image'),

    path('profile/<str:username>/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('home/post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post_detail'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


