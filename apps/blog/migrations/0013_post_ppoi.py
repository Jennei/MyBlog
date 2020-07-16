# Generated by Django 2.0.3 on 2018-08-08 23:15

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20180808_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20, verbose_name='封面 PPOI'),
        ),
    ]