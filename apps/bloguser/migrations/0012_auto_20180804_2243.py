# Generated by Django 2.0.3 on 2018-08-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloguser', '0011_userprofile_mobile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='邮箱'),
        ),
    ]