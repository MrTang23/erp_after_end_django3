# Generated by Django 4.2.4 on 2023-08-15 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False, verbose_name='产品id')),
                ('product_name', models.CharField(max_length=32, unique=True, verbose_name='产品名')),
                ('product_number', models.IntegerField(default=0, verbose_name='产品数量')),
            ],
        ),
    ]
