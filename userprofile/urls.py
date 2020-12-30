from django.urls import path
from . import views
from . import views_ajax as ajax_views

urlpatterns = [
    path('edit', views.edit_profile, name='edit_profile'),
    path('edit/profilephoto', ajax_views.change_profile_picture, name='change_profile_picture'),
    path('edit/coverphoto', ajax_views.change_cover_photo, name='change_cover_photo'),
    path('follow', ajax_views.toggle_user_follow, name='follow'),
]
