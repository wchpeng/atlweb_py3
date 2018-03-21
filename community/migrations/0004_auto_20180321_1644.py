# Generated by Django 2.0.1 on 2018-03-21 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0003_auto_20180207_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True, verbose_name='是否可见')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('name', models.CharField(max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='read_count',
            field=models.PositiveIntegerField(default=0, verbose_name='阅读数'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='community.BlogCategory'),
        ),
    ]
