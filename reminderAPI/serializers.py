from rest_framework import serializers
from . models import WeatherReminderUser, Reminder, Notification, Weather
from config.settings import WEATHER_API_URL, WEATHER_API_KEY, WEATHER_API_UNITS
import requests


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = WeatherReminderUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = WeatherReminderUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ('creation_date', 'city')
        # fields = '__all__'

    def create(self, validated_data):
        reminder = Reminder.objects.create(**validated_data)
        return reminder


class ReminderModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    owner_id = serializers.IntegerField()
    creation_date = serializers.DateTimeField()
    city = serializers.CharField(max_length=128)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('reminder', 'notification_type', 'receiver_uid', 'period', 'creation_date')

    def create(self, validated_data):
        notification = Notification.objects.create(**validated_data)
        return notification


class NotificationModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    reminder_id = serializers.IntegerField()
    creation_date = serializers.DateTimeField()
    notification_type = serializers.CharField(max_length=128)
    receiver_uid = serializers.CharField(max_length=128)
    period = serializers.CharField(max_length=128)


class WeatherDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("reminder", )

    def create(self, validated_data):
        url = f"{WEATHER_API_URL}?q={validated_data['reminder'].city}&units={WEATHER_API_UNITS}&APPID={WEATHER_API_KEY}"
        request_results = requests.get(url).json()
        if request_results['cod'] == 200:
            weather = Weather.objects.create(
                reminder=validated_data['reminder'],
                temp=request_results['main']['temp'],
                feels_like=request_results['main']['feels_like'],
                pressure=request_results['main']['pressure'],
                wind=request_results['wind']['speed'],
                visibility=request_results['visibility'],
                city=request_results['name']
            )
            return weather
        else:
            return request_results['cod']


class WeatherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    creation_date = serializers.DateTimeField()
    temp = serializers.FloatField()
    feels_like = serializers.FloatField()
    pressure = serializers.FloatField()
    wind = serializers.FloatField()
    visibility = serializers.CharField(max_length=300)
    city = serializers.CharField(max_length=300)
