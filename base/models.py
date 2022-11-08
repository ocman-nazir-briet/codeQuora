from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name[:20]
    class Meta:
        ordering=['name']

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-updated']

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]

    class Meta:
        ordering=['-updated']