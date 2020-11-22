from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add',views.AddPost.as_view(), name='add'),
    path('<str:username>/<slug:slug>/draft', views.draft, name='draft')
]