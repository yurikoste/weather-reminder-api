from django.contrib import admin
from . models import WeatherReminderUser, Reminder, Notification, Weather


# Register your models here.
admin.site.register(WeatherReminderUser)
admin.site.register(Reminder)
admin.site.register(Notification)
admin.site.register(Weather)
