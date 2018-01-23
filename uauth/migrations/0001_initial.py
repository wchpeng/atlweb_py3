# Generated by Django 2.0.1 on 2018-01-22 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('gender', models.BooleanField(default=1, verbose_name='性别')),
                ('user_hash', models.CharField(max_length=40, verbose_name='唯一标示')),
                ('birthday', models.DateTimeField(blank=True, null=True, verbose_name='生日')),
                ('mark', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='评分')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='地址')),
                ('signature', models.CharField(blank=True, max_length=50, null=True, verbose_name='签名')),
                ('username', models.CharField(blank=True, max_length=12, null=True, verbose_name='用户名')),
                ('avatar', models.ImageField(default='default_avatar.png', upload_to='avatar', verbose_name='头像')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
