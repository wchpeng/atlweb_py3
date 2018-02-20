# Generated by Django 2.0.1 on 2018-02-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0006_album_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, '多相册'), (2, '单相册')], default=1, null=True, verbose_name='相册类型'),
        ),
        migrations.AlterField(
            model_name='album',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='image.Picture', verbose_name='相册图片'),
        ),
    ]