from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.utils import timezone
import uuid
from django.db.models import signals
from apps.authentication.tasks import send_verification_email


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'authentication'
        db_table = 'User'

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('user name'), max_length=400, unique=True)
    full_name = models.CharField(_('full name'), max_length=400)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    date_joined = models.DateTimeField(default=timezone.now())
    verification_uuid = models.UUIDField(_('Unique verification UUID'), default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'username', 'full_name']

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.email


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)
