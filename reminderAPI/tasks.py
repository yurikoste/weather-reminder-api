from config.celery import app

from reminderAPI.models import Notification, Reminder, Weather, WeatherReminderUser
from services.notifications import send_notification_email
from services.retrievers import update_weather_from_server


@app.task
def send_notification():
    for reminder in Reminder.objects.all():
        notifications = reminder.notifications.all()
        for notification in notifications:
            user = WeatherReminderUser.objects.get(id=reminder.owner_id)
            weather = Weather.objects.get(reminder_id=reminder.pk)
            update_weather_from_server(reminder)
            send_notification_email(user.username, notification, weather)


@app.task
def send_beat_notification_3():
    for reminder in Reminder.objects.all():
        notifications = reminder.notifications.all()
        for notification in notifications:
            if notification.period == '3':
                user = WeatherReminderUser.objects.get(id=reminder.owner.id)
                weather = Weather.objects.get(reminder_id=reminder.pk)
                update_weather_from_server(reminder)
                send_notification_email(user.username, notification, weather)


@app.task
def send_beat_notification_6():
    for reminder in Reminder.objects.all():
        notifications = reminder.notifications.all()
        for notification in notifications:
            if notification.period == '6':
                user = WeatherReminderUser.objects.get(id=reminder.owner.id)
                weather = Weather.objects.get(reminder_id=reminder.pk)
                update_weather_from_server(reminder)
                send_notification_email(user.username, notification, weather)


@app.task
def send_beat_notification_12():
    for reminder in Reminder.objects.all():
        notifications = reminder.notifications.all()
        for notification in notifications:
            if notification.period == '12':
                user = WeatherReminderUser.objects.get(id=reminder.owner.id)
                weather = Weather.objects.get(reminder_id=reminder.pk)
                update_weather_from_server(reminder)
                send_notification_email(user.username, notification, weather)


@app.task
def send_beat_notification_24():
    for reminder in Reminder.objects.all():
        notifications = reminder.notifications.all()
        for notification in notifications:
            if notification.period == '24':
                user = WeatherReminderUser.objects.get(id=reminder.owner.id)
                weather = Weather.objects.get(reminder_id=reminder.pk)
                update_weather_from_server(reminder)
                send_notification_email(user.username, notification, weather)
