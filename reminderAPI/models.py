from django.db import models
from django.contrib.auth.models import AbstractUser


class WeatherReminderUser(AbstractUser):
    nick_name = models.CharField(max_length=128, blank=True, null=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"


class Reminder(models.Model):
    owner = models.ForeignKey(WeatherReminderUser, related_name="reminders", on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.owner} for {self.city}"


class Notification(models.Model):
    NOTIFICATION_BY = [
        ('email', 'email'),
    ]

    NOTIFICATION_PERIOD = [
        (3, 3),
        (6, 6),
        (12, 12),
        (24, 24),
    ]

    reminder = models.ForeignKey(Reminder, related_name="notifications", on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=128, choices=NOTIFICATION_BY, verbose_name='Notify by')
    receiver_uid = models.CharField(max_length=300, blank=True, null=True)
    period = models.CharField(max_length=32, choices=NOTIFICATION_PERIOD, verbose_name='Notify each ')
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reminder', 'notification_type', 'period',)

    def __str__(self):
        return f"by {self.notification_type} for {self.reminder.city} each {self.period} hours"


class Weather(models.Model):
    HOURS = (
        (3, 3),
        (6, 6),
        (12, 12),
        (24, 24)
    )

    reminder = models.ForeignKey(Reminder, related_name="weather_conditions", on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    temp = models.FloatField(verbose_name='Temperature in C', blank=True, null=True)
    feels_like = models.FloatField(verbose_name='Feels like in C', blank=True, null=True)
    pressure = models.FloatField(verbose_name='Pressure', blank=True, null=True)
    wind = models.FloatField(verbose_name='Wind m/s', blank=True, null=True)
    visibility = models.CharField(max_length=32, verbose_name='Pressure', blank=True, null=True)
    city = models.CharField(max_length=128, verbose_name='City', blank=True, null=True)

    def __str__(self):
        return f"Weather in {self.city} from {self.creation_date}"
