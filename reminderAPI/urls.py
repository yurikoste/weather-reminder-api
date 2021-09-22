from django.urls import path
from reminderAPI import views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'reminderAPI'

urlpatterns = [
    path('registration/', views.Registration.as_view(), name='registration'),
    path('create_reminder/', views.CreateReminder.as_view(), name='create_reminder'),
    path('list_reminders/', views.ReminderListView.as_view(), name='list_reminders'),
    path('delete_reminder/<int:pk>', views.ReminderDeleteView.as_view(), name='delete_reminder'),
    path('create_notification/', views.CreateNotification.as_view(), name='create_notification'),
    path('list_notifications/', views.NotificationListView.as_view(), name='list_notifications'),
    path('edit_notification/<int:pk>', views.NotificationEditView.as_view(), name='edit_notification'),
    path('list_weather/', views.WeatherListView.as_view(), name='list_weather'),
    path('request_weather/<int:pk>', views.WeatherView.as_view(), name='request_weather'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
