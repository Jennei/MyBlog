# Generated by Django 2.0.3 on 2018-08-04 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloguser', '0012_auto_20180804_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True, verbose_name='邮箱'),
            preserve_default=False,
        ),
    ]
