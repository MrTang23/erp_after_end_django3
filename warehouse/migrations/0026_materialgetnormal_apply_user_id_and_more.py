# Generated by Django 4.2.4 on 2023-08-18 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0025_remove_linkmaterialgetnormal_material_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialgetnormal',
            name='apply_user_id',
            field=models.IntegerField(default=3, verbose_name='申请人id'),
        ),
        migrations.AddField(
            model_name='materialgetnormal',
            name='create_time',
            field=models.CharField(default='未填写', max_length=32, verbose_name='申请创建时间'),
        ),
        migrations.AlterField(
            model_name='linkmaterialgetnormal',
            name='material_weight',
            field=models.FloatField(verbose_name='材料领取重量'),
        ),
    ]