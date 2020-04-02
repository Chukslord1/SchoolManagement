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
    secret_pin = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username
NULL_AND_BLANK = {'null': True, 'blank': True}
class UnusedPins(models.Model):
    pin = models.CharField(max_length=12)

class UsedPins(models.Model):
    pin = models.CharField(max_length=12)
#use auth to check if the pin is in the unusedpin and in the used pinwhen your posting what the users are going to use
