from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    user_type = (
        ('Parent', 'Parent'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
        ('Accountant', 'Accountant'),
        ('Liberian', 'Liberian'),

    )

    def __str__(self):
        return self.user.username
