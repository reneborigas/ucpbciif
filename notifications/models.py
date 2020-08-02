from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Notification(models.Model):
    action_time = models.DateTimeField(
        auto_now_add=True,
    )
    committee = models.ForeignKey(
        'committees.Committee',
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    action_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    message = models.CharField(
        max_length=255, 
        blank=False
    )
    link = models.CharField(
        max_length=255, 
        blank=False
    )

    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name="notification_content_type",
        blank=True,
        null = True,
    )

    object_id = models.PositiveIntegerField(
        blank=True,
        null = True,
    )

    content_object = GenericForeignKey(
        'content_type', 
        'object_id',
    )
    object_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    isViewed = models.BooleanField(
        default=False,
    )
    # apiLink = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null = True,
    # )
    # valueToDisplay = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null = True,
    # )

    def __str__(self):
        return "%s - %s %s %s" % (self.committee,self.action_type, self.content_type, self.object_id)


class NotificationView(models.Model):
    committee = models.ForeignKey(
        'committees.Committee',
        on_delete=models.CASCADE,
        related_name="viewedNotifcations",
        blank=True,
        null = True,
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notificationViewers"
    )
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name="viewedNotifcations",
        blank=True,
        null = True,
    )


    def __str__(self):
        return "%s - %s" % (self.committee,self.notification)
