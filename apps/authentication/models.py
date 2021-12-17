from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.db.models import signals
from apps.authentication.tasks import send_verification_email


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email address must be provided'))

        if not password:
            raise ValueError(_('Password must be provided'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserAccountManager()

    email = models.EmailField(_('email'), unique=True, blank=False, null=False)
    username = models.CharField(_('user name'), max_length=400, unique=True, blank=True, null=True)
    full_name = models.CharField(_('full name'), max_length=400, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=False)
    verification_uuid = models.UUIDField(_('Unique verification UUID'), default=uuid.uuid4)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=User)