# Generated by Django 4.2.4 on 2023-08-21 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_linkproductionorderbyproduct_product_second_received_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionorder',
            name='deputy_general_manager_confirm',
            field=models.IntegerField(default=2, verbose_name='副总确认'),
        ),
        migrations.AlterField(
            model_name='productionorder',
            name='production_control_upload',
            field=models.IntegerField(default=2, verbose_name='生管上传'),
        ),
    ]