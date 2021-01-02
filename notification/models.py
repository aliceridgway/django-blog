from django.db import models
from userprofile.models import Profile
from abc import abstractmethod


class Notification(models.Model):
    profile = models.ForeignKey(Profile, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} | {self.message}'


class Event(models.Model):
    user_from = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="%(class)s_activities")
    user_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="%(class)s_notifications")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @abstractmethod
    def get_notification_str(self):
        pass


class Follow(Event):

    def __str__(self):
        return f"{self.user_from.user.username} followed {self.user_to.user.username}"

    def get_notification_str(self):
        return f"{self.user_from.user.username} followed you."
