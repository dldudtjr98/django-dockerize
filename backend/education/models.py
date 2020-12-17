from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cert.models import CustomUser


def thumbnail_directory_path(instance, filename):
    return settings.THUMBNAIL_URL + f'user_{instance.user_id}/{filename}.jpg'


class CurriculumDivision(models.Model):
    name = models.CharField(_("분류명"), max_length=30)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'education_curriculum_division'
        verbose_name = '커리큘럼분류'
        verbose_name_plural = '커리큘럼분류'


class Curriculum(models.Model):
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(_('제목'), max_length=50, unique=True)
    classification = models.ForeignKey(CurriculumDivision, on_delete=models.SET_NULL, null=True)
    password = models.CharField(_('수강비밀번호'), max_length=10)
    thumbnail = models.ImageField(  # default image in app/static/image/profile
        _('섬네일이미지'),
        upload_to=thumbnail_directory_path,
        default=settings.THUMBNAIL_URL + settings.DEFAULT_THUMBNAIL_IMAGE
    )
    subject = models.TextField(_('주제'))
    public = models.BooleanField(_('공개여부'), default=True)
    contents = models.TextField(_('내용'))
    reg_time = models.DateTimeField(_('등록시간'), auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = '커리큘럼'
        verbose_name_plural = '커리큘럼들'
