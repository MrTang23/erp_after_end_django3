# Generated by Django 4.2.4 on 2023-08-13 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_alter_rawmaterial_material_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialPurchase',
            fields=[
                ('material_purchase_id', models.AutoField(primary_key=True, serialize=False, verbose_name='原料采购单id')),
                ('apply_user_id', models.IntegerField(verbose_name='申请人id')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='申请创建时间')),
                ('delivery_note_img', models.ImageField(upload_to='img_url/', verbose_name='送货单')),
                ('warehousing_entry_img', models.ImageField(upload_to='img_url/', verbose_name='入库单')),
                ('quality_confirm', models.IntegerField(default=0, verbose_name='品控确认')),
                ('warehousing_confirm', models.IntegerField(default=0, verbose_name='仓库确认')),
            ],
        ),
    ]