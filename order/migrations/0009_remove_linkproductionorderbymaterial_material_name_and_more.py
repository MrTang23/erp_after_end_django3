# Generated by Django 4.2.4 on 2023-08-16 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_productionorder_custom_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkproductionorderbymaterial',
            name='material_name',
        ),
        migrations.AddField(
            model_name='linkproductionorderbymaterial',
            name='material_id',
            field=models.IntegerField(default=0, verbose_name='材料id'),
        ),
        migrations.AddField(
            model_name='linkproductionorderbyproduct',
            name='if_semi_finished',
            field=models.IntegerField(default=0, verbose_name='是否半成品'),
        ),
    ]