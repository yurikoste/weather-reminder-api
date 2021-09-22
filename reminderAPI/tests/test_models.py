from django.test import TestCase, Client
from reminderAPI.serializers import *


class ModelsTests(TestCase):
    def setUp(self):
        self.user = WeatherReminderUser.objects.create(
            password='aA987654321',
            email='test@example.com',
            username='user0'
        )
        self.client = Client()

    def test_User_model(self):
        self.user = WeatherReminderUser.objects.create(
            email='myemail@test.com',
            password='aA987654321',
            username='user'
        )

    def test_Reminder_Model(self):
        self.reminder = Reminder.objects.create(
            city='London',
            owner=self.user
        )

    def test_Notification_Model(self):
        self.reminder = Reminder.objects.create(
            city='London',
            owner=self.user
        )

        self.notification = Notification.objects.create(
            reminder=self.reminder,
            notification_type='email',
            receiver_uid='12345',
            period='3'
        )

    def test_Weather_model(self):
        self.reminder = Reminder.objects.create(
            city='London',
            owner=self.user
        )

        self.weather = Weather.objects.create(
            reminder=self.reminder,
            temp=25,
            feels_like=27,
            pressure=1000,
            wind=3,
            visibility=100,
            city='London'
        )

    def tearDown(self):
        self.user = WeatherReminderUser.objects.create(
            password='aA987654321',
            email='test@example.com',
            username='user1'
        )
        self.user.delete()
