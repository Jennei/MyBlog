# Generated by Django 2.0.3 on 2018-08-19 18:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='订单编号')),
                ('trade_sn', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='第三方交易编号')),
                ('status', models.CharField(choices=[('complete', '已支付订单'), ('un_complete', '未支付订单'), ('cancel', '订单取消')], default='un_complete', max_length=20, verbose_name='支付状态')),
                ('order_amount', models.FloatField(default=0, verbose_name='订单金额')),
                ('payment_type', models.CharField(choices=[('alipay', '支付宝'), ('weichat', '微信')], default='alipay', max_length=20, verbose_name='支付方式')),
                ('pay_time', models.DateTimeField(default=None, verbose_name='支付时间')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='订单留言')),
                ('signer_name', models.CharField(max_length=30, verbose_name='签收人称呼')),
                ('signer_phone_num', models.CharField(max_length=14, verbose_name='联系电话')),
                ('sign_time', models.DateTimeField(default=None, verbose_name='签收时间')),
                ('address', models.CharField(max_length=300, verbose_name='寄送地址')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='订单创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='付费用户')),
            ],
            options={
                'verbose_name': '商品订单信息',
                'verbose_name_plural': '商品订单信息',
            },
        ),
        migrations.CreateModel(
            name='GoodsOrderReleation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='关联商品id')),
                ('n_goods', models.PositiveIntegerField(default=0, verbose_name='商品购买数量')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='关联商品内容类型')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.GoodsOrder', verbose_name='关联订单')),
            ],
            options={
                'verbose_name': '订单商品关系',
                'verbose_name_plural': '订单商品关系',
            },
        ),
        migrations.CreateModel(
            name='PaymentLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_sn', models.CharField(max_length=50, unique=True, verbose_name='商品序列号')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('goods_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.GoodsOrderReleation', verbose_name='关联订单')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='付费用户')),
            ],
            options={
                'verbose_name': '商品支付记录',
                'verbose_name_plural': '商品支付记录',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='商品id')),
                ('n_goods', models.PositiveIntegerField(default=1, verbose_name='商品购买数量')),
                ('created_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='商品类型')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='付费用户')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
            },
        ),
    ]
