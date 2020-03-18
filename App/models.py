from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    USER_TYPE_CHOICES = (
        ('Parent', 'Parent'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
        ('Accountant', 'Accountant'),
        ('Liberian', 'Liberian'),

    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    secret_pin = models.IntegerField()

    def __str__(self):
        return self.user.username
