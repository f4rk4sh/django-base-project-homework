import logging
from settings.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

UserModel = get_user_model()


@app.task
def send_verification_email(user_id):
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your Django-base-proj account',
            'Follow this link to verify your account: '
            f'http://18.224.139.103/{reverse("verify", kwargs={"uuid": str(user.verification_uuid)})}',
            'a4086308@gmail.com',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning(f"Tried to send verification email to non-existing user '{user_id}'")
