# Generated by Django 2.0.1 on 2018-01-28 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('content', models.CharField(max_length=512, verbose_name='内容')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name_plural': '回复',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('content', models.CharField(max_length=512, verbose_name='内容')),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='image.Album', verbose_name='图册')),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='image.Picture', verbose_name='图片')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name_plural': '评论',
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.Review'),
        ),
        migrations.AddField(
            model_name='reply',
            name='source',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.Reply'),
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]