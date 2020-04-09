from django.db import models
from django.contrib.auth.models import User

# Create your models here
NULL_AND_BLANK = {'null': True, 'blank': True}
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    name = models.TextField()
    #for student adding just make the usertpe to be equal to student in reg without any if or for stetment
    parent = models.CharField(max_length=100, **NULL_AND_BLANK)
    class_room = models.CharField(max_length=100, **NULL_AND_BLANK)
    section = models.CharField(max_length=100, **NULL_AND_BLANK)
    session = models.CharField(max_length=100, **NULL_AND_BLANK)
    gender = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100, **NULL_AND_BLANK)
    birthday = models.CharField(max_length=100 ,**NULL_AND_BLANK)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    image = models.ImageField()

    USER_TYPE_CHOICES = (
        ('Parent', 'Parent'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
        ('Accountant', 'Accountant'),
        ('Liberian', 'Liberian'),

    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES)
    secret_pin = models.CharField(max_length=12, **NULL_AND_BLANK)

    def __str__(self):
        return self.user.username
class BulkStudent(models.Model):
    name = models.TextField()
    #for student adding just make the usertpe to be equal to student in reg without any if or for stetment
    parent = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email= models.EmailField()
    password = models.TextField()


class UnusedPins(models.Model):
    pin = models.CharField(max_length=12)

class UsedPins(models.Model):
    pin = models.CharField(max_length=12)
#use auth to check if the pin is in the unusedpin and in the used pinwhen your posting what the users are going to use
