# Generated by Django 4.2.4 on 2023-08-19 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0026_materialgetnormal_apply_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkmaterialgetnormal',
            name='material_get_id',
            field=models.IntegerField(default=0, verbose_name='材料领取id'),
        ),
    ]
