# Generated by Django 4.2.4 on 2023-08-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_productionorder_deputy_general_manager_confirm_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productionorder',
            name='deputy_general_manager_confirm',
        ),
        migrations.RemoveField(
            model_name='productionorder',
            name='deputy_general_manager_confirm_time',
        ),
        migrations.RemoveField(
            model_name='productionorder',
            name='production_control_upload',
        ),
        migrations.RemoveField(
            model_name='productionorder',
            name='production_control_upload_time',
        ),
        migrations.AddField(
            model_name='productionorder',
            name='factory_manager_confirm',
            field=models.IntegerField(default=2, verbose_name='厂长确认'),
        ),
        migrations.AddField(
            model_name='productionorder',
            name='factory_manager_confirm_time',
            field=models.CharField(default='yyyy-mm-dd hh:mm:ss', max_length=32, verbose_name='厂长确认时间'),
        ),
    ]