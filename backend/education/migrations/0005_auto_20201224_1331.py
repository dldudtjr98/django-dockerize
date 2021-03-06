# Generated by Django 3.1.3 on 2020-12-24 04:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20201224_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculumlecture',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='등록일'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curriculumprogress',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='학습 완료일'),
        ),
        migrations.AlterField(
            model_name='curriculumstudent',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='등록일'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='url',
            field=models.URLField(verbose_name='영상 주소'),
        ),
    ]
