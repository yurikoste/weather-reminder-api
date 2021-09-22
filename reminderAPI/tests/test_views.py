from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory
from reminderAPI.views import *
from reminderAPI.serializers import *


class ViewsTesting(TestCase):
    def setUp(self):
        self.user = WeatherReminderUser.objects.create(password='aA987654321', username='test_user')
        self.client = Client()

    def test_registration(self):
        data = {
            'password': '12345',
            'username': 'test'
        }
        response = self.client.post('/api/v1/registration/', data)
        self.assertEqual(response.status_code, 200)

    def test_create_reminder_without_auth(self):
        data = {
            'city': 'Prague'
        }
        response = self.client.post("/api/v1/create_reminder/", data)
        self.assertEqual(response.status_code, 403)

    def test_create_reminder(self):
        factory = APIRequestFactory()
        user = WeatherReminderUser.objects.get(username='test_user')
        view = CreateReminder.as_view()

        data = {
            'city': 'Prague',
            'owner': user,
        }

        request = factory.post('api/v1/create_reminder/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_list_reminders(self):
        user = WeatherReminderUser.objects.get(username='test_user')
        reminder = Reminder.objects.create(
            city='London',
            owner=user
        )
        factory = APIRequestFactory()
        view = ReminderListView.as_view()
        request = factory.get('api/v1/list_reminders/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_delete_reminder(self):
        factory = APIRequestFactory()
        user = WeatherReminderUser.objects.get(username='test_user')
        view = ReminderDeleteView.as_view()

        self.reminder = Reminder.objects.create(
            owner=self.user,
            city='London'
        )

        request = factory.delete(f"api/v1/edit_reminder/{self.reminder.id}/")
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.reminder.id)
        self.assertEqual(response.status_code, 204)

    def test_create_notification(self):
        factory = APIRequestFactory()
        self.user = WeatherReminderUser.objects.get(username='test_user')

        # Create reminder which will be updated within CreateNotification view
        view = CreateReminder.as_view()
        data = {
            'city': 'Prague',
            'owner': self.user,
        }
        request = factory.post('api/v1/create_reminder/', data)
        force_authenticate(request, user=self.user)
        response = view(request)

        # Test for CreateNotification view
        view = CreateNotification.as_view()
        self.reminder = Reminder.objects.get(owner=self.user, city='Prague')

        data = {
            'reminder': self.reminder.id,
            'notification_type': 'email',
            'receiver_uid': '12345',
            'period': '6',
            'city': self.reminder.city,
        }

        request = factory.post('api/v1/create_notification/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
