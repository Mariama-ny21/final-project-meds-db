from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_healthcare_professional = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username} (Healthcare: {self.is_healthcare_professional})"
