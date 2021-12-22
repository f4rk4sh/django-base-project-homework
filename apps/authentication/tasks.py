import settings.base
from config.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@app.task
def send_verification_email(subject, message, recipient):
    send_mail(subject, message, settings.base.EMAIL_HOST_USER, [recipient], fail_silently=False)
