from django.urls import path
from . import views
from . import views_ajax

urlpatterns = [
    path('add', views.AddPost.as_view(), name='add'),
    path('comment', views_ajax.add_comment, name='add_comment'),
    path('<str:username>', views.author, name='author'),
    path('<str:username>/<slug:slug>', views.post_detail, name='post_detail'),
    path('<str:username>/<slug:slug>/draft', views.draft, name='draft'),
    path('<str:username>/<slug:slug>/edit', views.EditPost.as_view(), name='edit_post'),
    path('<str:username>/<slug:slug>/publish', views.publish_post, name='publish_post'),
    path('<str:username>/<slug:slug>/delete', views.DeletePost.as_view(), name='delete_post'),
]
