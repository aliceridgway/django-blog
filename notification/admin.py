from django.contrib import admin
from .models import Like, Follow, Comment, Notification
# Register your models here.

admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Notification)
