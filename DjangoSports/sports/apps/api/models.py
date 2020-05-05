from django.db import models
from apps.authentication.models import User

class League(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    conference = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
