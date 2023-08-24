# Generated by Django 4.2.4 on 2023-08-16 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0016_alter_rawmaterial_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rawmaterial',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='rawmaterial',
            name='material_type',
            field=models.CharField(default='6414', max_length=32, unique=True, verbose_name='材料型号'),
        ),
        migrations.AlterUniqueTogether(
            name='rawmaterial',
            unique_together={('material_name', 'material_supplier', 'material_product_supplier', 'material_type')},
        ),
    ]
