# Generated by Django 3.0 on 2023-08-12 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='User',
        ),
    ]
