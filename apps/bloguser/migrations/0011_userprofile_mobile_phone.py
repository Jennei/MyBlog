# Generated by Django 2.0.3 on 2018-08-04 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloguser', '0010_auto_20180802_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile_phone',
            field=models.CharField(default='', max_length=14, verbose_name='手机号码'),
        ),
    ]
