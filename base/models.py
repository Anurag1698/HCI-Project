from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", null=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # pass


class Topic(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="image", null=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/assets/img/banner1.jpg"

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="image", null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name[0:50]


class Curriculam(models.Model):
    name = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to="files", blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name[0:50]


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]


class Blog(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="image", null=True)
    name = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name[0:50]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]


class RoomRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} request for {self.room.name}"


class RoomNotification(models.Model):
    NOTIFICATION_TYPES = [
        ("joined", "Joined"),
        ("rejected", "Rejected"),
        ("removed", "Removed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.room.name}"
