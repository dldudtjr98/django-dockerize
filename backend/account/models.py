from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


def profile_directory_path(instance, filename):
    return 'static/image/profile/user_{}/{}'.format(instance.name, filename)

class UserManager(BaseUserManager):

    use_in_migrations = True
    def create_user(self, user_id, email, name, nickname, profile_image, password=None):

        if not user_id :
            raise ValueError('must have user id')
        user = self.model(
            user_id = user_id,
            name = name,
            email = self.normalize_email(email),
            nickname = nickname,
            profile_image = profile_image,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, name, nickname, password):        
       
        user = self.create_user(
            user_id = user_id,
            name = name,
            email = self.normalize_email(email),
            nickname = nickname,            
            password = password,
            profile_image = '',
        )        
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):    
    
    objects = UserManager()
    
    user_id = models.CharField(
        max_length=15,
        null=False,
        unique=True,
        verbose_name='ID',
    )
    name = models.CharField(
        max_length=20,
        null=False,
        verbose_name='이름',
    )
    email = models.EmailField(        
        max_length=255,
        unique=True,
        verbose_name='이메일',
    )    
    nickname = models.CharField(
        max_length=20,
        null=False,
        unique=True,
        verbose_name='닉네임',
    )
    profile_image = models.ImageField(
        default='static/image/profile/user_testman_test',
        upload_to=profile_directory_path,
        verbose_name='프로필사진',
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화') # necessary
    is_admin = models.BooleanField(default=False, verbose_name='관리자') # necessary
    note_receive = models.BooleanField(default=True, verbose_name='쪽지수신')
    mail_receive = models.BooleanField(default=True, verbose_name='메일수신')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')
    last_login = models.DateTimeField(verbose_name='마지막 로그인일자')
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'email', 'nickname']

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


    class Meta:
        db_table = 'account_custom_user'
        verbose_name = '유저'
        verbose_name_plural = '유저들'