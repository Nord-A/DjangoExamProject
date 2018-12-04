# Generated by Django 2.1.3 on 2018-12-04 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000)),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('datetime_edited', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('question', models.TextField(max_length=2000)),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('datetime_edited', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('views_count', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumps_up', models.BooleanField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Comment')),
                ('thread', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.ForumThread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='forumthread',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.ForumThread'),
        ),
    ]
