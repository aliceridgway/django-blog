from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add',views.AddPost.as_view(), name='add'),
    path('<str:username>/<slug:slug>/draft', views.draft, name='draft'),
    path('<str:username>/<slug:slug>/edit', views.EditPost.as_view(), name='edit_post'),
    path('<str:username>/<slug:slug>/publish', views.publish_post, name='publish_post')
]