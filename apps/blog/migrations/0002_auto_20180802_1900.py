# Generated by Django 2.0.3 on 2018-08-02 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='博文作者'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cover_url',
            field=models.CharField(blank=True, help_text='不写默认为默认封面url', max_length=255, null=True, verbose_name='博文封面url'),
        ),
    ]
