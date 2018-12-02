# Generated by Django 2.1.3 on 2018-12-02 14:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='forumthread',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='forumthread',
            name='datetime_edited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='forumthread',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='forumuser',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
