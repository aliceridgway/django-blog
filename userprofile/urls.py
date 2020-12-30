from django.urls import path
from . import views
from . import views_ajax as ajax_views

urlpatterns = [
    path('<str:username>/edit', views.edit_profile, name='edit_profile'),
    path('<str:username>/profile/photo/change', ajax_views.change_profile_picture, name='change_profile_picture'),
    path('coverphoto', ajax_views.change_cover_photo, name='change_cover_photo'),
    path('follow', ajax_views.toggle_user_follow, name='follow'),
]
