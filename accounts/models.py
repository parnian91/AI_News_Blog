from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    # website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

