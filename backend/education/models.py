from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from cert.models import CustomUser


def thumbnail_directory_path(instance, filename):
    return settings.THUMBNAIL_URL + f'user_{instance.user_id}/{filename}.jpg'


class CurriculumDivision(models.Model):
    name = models.CharField(_("분류명"), max_length=30)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'education_curriculum_division'
        verbose_name = '커리큘럼분류'
        verbose_name_plural = '커리큘럼분류'


class Curriculum(models.Model):
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='curriculum_founder')
    title = models.CharField(_('제목'), max_length=50, unique=True)
    students = models.ManyToManyField(CustomUser, through='CurriculumStudent', related_name='curriculum_student')
    division = models.ForeignKey(
        CurriculumDivision,
        on_delete=models.CASCADE,
    )
    password = models.CharField(_('수강비밀번호'), max_length=128, blank=True)
    thumbnail = models.ImageField(  # default image in app/static/image/profile
        _('섬네일이미지'),
        upload_to=thumbnail_directory_path,
        default=settings.THUMBNAIL_URL + settings.DEFAULT_THUMBNAIL_IMAGE
    )
    subject = models.TextField(_('주제'))
    public = models.BooleanField(_('공개여부'), default=True)
    contents = models.TextField(_('내용'), blank=True)
    start_date = models.DateTimeField(_('시작시간'))
    end_date = models.DateTimeField(_('종료시간'))
    reg_date = models.DateTimeField(_('등록일'), auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = '커리큘럼'
        verbose_name_plural = '커리큘럼'


class LectureDivision(models.Model):
    name = models.CharField(_('분류명'), max_length=30)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'education_lecture_division'


class Lecture(models.Model):
    DIFFICULTY_CHOICE = (
        ('B', 'Basic'),
        ('D', 'Deep'),
    )
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lecture_founder')
    title = models.CharField(_('제목'), max_length=50, unique=True)
    curriculum = models.ManyToManyField(Curriculum, through='CurriculumLecture')
    division = models.ForeignKey(
        LectureDivision,
        on_delete=models.CASCADE,
    )
    difficulty = models.CharField(_('난이도'), max_length=10, choices=DIFFICULTY_CHOICE)
    goal = models.CharField(_('학습목표'), max_length=100, blank=True)
    method = models.TextField(_('학습방법'), blank=True)
    main_contents = models.CharField(_('주요 컨텐츠'), max_length=100, blank=True)
    effect = models.CharField(_('기대효과'), max_length=100, blank=True)
    public = models.BooleanField(_('공개여부'), default=True)
    contents = models.TextField(_('내용'), blank=True)
    reg_date = models.DateTimeField(_('등록일'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = '강좌'
        verbose_name_plural = '강좌'


class Lesson(models.Model):
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_founder')
    title = models.CharField(_('제목'), max_length=50, unique=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    outline = models.CharField(_('개요'), max_length=100, blank=True)
    url = models.URLField(_('영상 주소'))
    duration = models.IntegerField(_('강의 시간'))
    public = models.BooleanField(_('공개여부'), default=True)
    contents = models.TextField(_('내용'), blank=True)
    ordering = models.IntegerField(_('순서'))
    reg_date = models.DateTimeField(_('등록일'), auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = '강의'
        verbose_name_plural = '강의'


class CurriculumLecture(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    start_date = models.DateTimeField(_('시작일'))
    end_date = models.DateTimeField(_('종료일'))
    ordering = models.IntegerField(_('순서'))
    reg_date = models.DateTimeField(_('등록일'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'education_curriculum_lecture'


class CurriculumStudent(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(_('등록일'), auto_now_add=True)

    class Meta:
        db_table = 'education_curriculum_student'


class CurriculumProgress(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date = models.DateTimeField(_('학습 완료일'), auto_now_add=True)

    class Meta:
        db_table = 'education_curriculum_progress'
