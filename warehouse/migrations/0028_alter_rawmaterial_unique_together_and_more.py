# Generated by Django 4.2.4 on 2023-08-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0027_linkmaterialgetnormal_material_get_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rawmaterial',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='rawmaterial',
            name='material_color',
            field=models.CharField(default='颜色', max_length=10, verbose_name='颜色'),
        ),
        migrations.AlterUniqueTogether(
            name='rawmaterial',
            unique_together={('material_name', 'material_type', 'material_color', 'material_supplier', 'material_product_supplier')},
        ),
    ]
