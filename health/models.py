

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class HealthReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    symptoms = models.TextField()
    medical_history = models.TextField()
    lifestyle = models.TextField()
    description = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.user.email} on {self.created_at.strftime('%Y-%m-%d')}"
