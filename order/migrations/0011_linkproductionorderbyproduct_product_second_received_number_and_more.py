# Generated by Django 4.2.4 on 2023-08-20 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_productionorder_production_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkproductionorderbyproduct',
            name='product_second_received_number',
            field=models.IntegerField(default=0, verbose_name='产品重工入库数量'),
        ),
        migrations.AddField(
            model_name='linkproductionorderbyproduct',
            name='product_second_shipped_number',
            field=models.IntegerField(default=0, verbose_name='产品重工出库数量'),
        ),
    ]