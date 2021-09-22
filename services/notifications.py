from django.template.loader import render_to_string
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from config import settings


def send_notification_email(user, notification, weather):
    email_subject = f'Weather in {notification.reminder.city}'
    email_body = render_to_string('weather_email.html', {
        'user': user,
        'city': notification.reminder.city,
        'weather': weather
    })

    message = Mail(
        from_email=settings.EMAIL_FROM_USER,
        to_emails=[notification.receiver_uid],
        subject=email_subject,
        html_content=email_body
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return 'Successful sending'
    except Exception as e:
        return 'ERROR'

