from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_name = models.CharField(max_length=100)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["createdDate"]

class UserJoined(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)