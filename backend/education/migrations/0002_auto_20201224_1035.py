# Generated by Django 3.1.3 on 2020-12-24 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='division',
            field=models.ForeignKey(default=(), on_delete=django.db.models.deletion.SET_DEFAULT, to='education.lecturedivision'),
        ),
    ]
