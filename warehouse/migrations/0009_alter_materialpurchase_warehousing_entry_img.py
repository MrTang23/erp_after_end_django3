# Generated by Django 4.2.4 on 2023-08-14 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_linkmaterialpurchase_material_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialpurchase',
            name='warehousing_entry_img',
            field=models.CharField(default='empty', max_length=32, verbose_name='入库单'),
        ),
    ]
