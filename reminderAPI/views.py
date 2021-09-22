from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import generics
from services.retrievers import get_weather_from_server, update_weather_from_server
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from services.notifications import send_notification_email
from reminderAPI.models import Weather
from .tasks import send_notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class Registration(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })


class CreateReminder(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ReminderSerializer

    def post(self, request, *args, **kwargs):
        user = WeatherReminderUser.objects.get(id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        request.data._mutable = True
        request.data['city'] = request.data.get('city', "No city was selected").title()
        request.data._mutable = False
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        reminder = serializer.save()
        reminder.save()
        weather = get_weather_from_server(reminder)
        if weather['response'] != 'Weather was successfully added to DB':
            return Response({
                'weather_server_code_error': weather['response']
            })
        return Response({
            "reminder": ReminderSerializer(reminder, context=self.get_serializer_context()).data,
        })


class ReminderListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ReminderModelSerializer

    def get_queryset(self):
        return Reminder.objects.filter(owner=self.request.user)


class ReminderDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ReminderSerializer
    queryset = Reminder.objects.all()


class CreateNotification(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()
        notification.save()
        weather_status = update_weather_from_server(notification.reminder)
        weather = Weather.objects.get(reminder_id=notification.reminder.pk)
        if notification.notification_type == 'email':
            res = send_notification_email(request.user, notification, weather)
        return Response({
            "notification": NotificationSerializer(notification, context=self.get_serializer_context()).data,
        })


class NotificationListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = NotificationModelSerializer
    queryset = Notification.objects.all()


class NotificationEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


class WeatherListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = WeatherSerializer

    def get_queryset(self):
        users_reminders = Reminder.objects.filter(owner=self.request.user)
        return Weather.objects.filter(id__in=users_reminders.values_list('weather_conditions', flat=True))


class WeatherView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()

    def get(self, request, *args, **kwargs):
        Weather.objects.filter(pk=kwargs['pk'])
        return self.retrieve(request, *args, **kwargs)

