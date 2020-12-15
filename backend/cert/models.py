from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def profile_directory_path(instance, filename):
    return settings.PROFILE_URL + f'user_{instance.user_id}/{filename}.jpg'

class UserManager(BaseUserManager):
    def create_user(self, user_id, email, name, password=None):
        if not user_id:
            raise ValueError("User must have a user id")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.user_id = user_id
        user.name = name
        user.set_password(password)  # change password to hash
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_id, email, name, password=None):
        if not user_id:
            raise ValueError("User must have a user id")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.user_id = user_id
        user.name = name
        user.set_password(password)  # change password to hash
        user.is_admin = False
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, name, password=None):
        if not user_id:
            raise ValueError("User must have a user id")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.user_id = user_id
        user.name = name
        user.set_password(password)  # change password to hash
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):    
    ADMIN = 'admin'
    STAFF = 'staff'
    STATUS = [
        (ADMIN, _('Admin User')),
        (STAFF, _('Staff User')),
    ]
    user_id = models.CharField(_('user_id'), max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30)
    nickname = models.CharField(_('nickname'), max_length=10, unique=True)
    profile_image = models.ImageField( #default image in app/static/image/profile
        _('profile_image'), 
        upload_to=profile_directory_path, 
        default=settings.PROFILE_URL + settings.DEFAULT_PROFILE_IMAGE) 
    mail_service = models.BooleanField(_('mail_service'), default=True)
    note_receive = models.BooleanField(_('note_reveive'), default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_admin = models.BooleanField(default=False)
    reg_time = models.DateTimeField(_('register_time'),auto_now_add=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'email',]

    objects = UserManager()

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "{}".format(self.user_id)

    class Meta:
        db_table = 'cert_custom_user'
        verbose_name = '유저'
        verbose_name_plural = '유저들'