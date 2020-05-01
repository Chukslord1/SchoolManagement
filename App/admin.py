from django.contrib import admin
from .models import UserProfile, UnusedPins, UsedPins, BulkStudent, AttendClass

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UnusedPins)
admin.site.register(UsedPins)
admin.site.register(BulkStudent)
admin.site.register(AttendClass)
