# Generated by Django 2.0.3 on 2018-08-19 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20180819_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsorderreleation',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_list', to='trade.GoodsOrder', verbose_name='关联订单'),
        ),
    ]
