# Generated by Django 2.0.1 on 2018-02-07 13:35

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('title', models.CharField(max_length=32)),
                ('content', ckeditor.fields.RichTextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
