# Generated by Django 2.0.3 on 2018-05-06 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloguser', '0003_auto_20180505_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
