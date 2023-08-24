from django.db import models


# Create your models here.
# 产品基本表
class Product(models.Model):
    product_id = models.AutoField(verbose_name='产品id', primary_key=True)
    product_name = models.CharField(verbose_name='产品名', max_length=32, unique=True)
    product_number = models.IntegerField(verbose_name='产品数量', default=0)
    product_semi_finished_number = models.IntegerField(verbose_name='半成品数量', default=0)
    shelf_number = models.CharField(verbose_name='货架号', default='无', max_length=10)


# 产品入库表
class ProductStorageNormal(models.Model):
    product_storage_id = models.AutoField(verbose_name='产品入库id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id', default=3)
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32, default='未填写')
    production_order_id = models.CharField(verbose_name='生产指令单id', max_length=32)
    quality_confirm = models.IntegerField(verbose_name='品控确认', default=0)
    product_storage_img = models.CharField(verbose_name='产品入库单', max_length=32)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    quality_confirm_time = models.CharField(verbose_name='品控确认时间', max_length=32,
                                            default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 连接产品入库表
class LinkProductStorageNormal(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    product_storage_id = models.IntegerField(verbose_name='产品入库id', default=0)
    product_name = models.CharField(verbose_name='产品名', default=0, max_length=32)
    product_number = models.FloatField(verbose_name='产品数量', default=0)


# 产品出货表
class ProductShipmentNormal(models.Model):
    product_shipment_id = models.AutoField(verbose_name='产品出货id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id', default=3)
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32, default='未填写')
    production_order_id = models.CharField(verbose_name='生产指令单id', max_length=32)
    quality_confirm = models.IntegerField(verbose_name='品控确认', default=0)
    product_shipment_img = models.CharField(verbose_name='产品入库单', max_length=32)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    quality_confirm_time = models.CharField(verbose_name='品控确认时间', max_length=32,
                                            default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 连接产品出货表
class LinkProductShipmentNormal(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    product_shipment_id = models.IntegerField(verbose_name='产品出货id', default=0)
    product_name = models.CharField(verbose_name='产品名', default=0, max_length=32)
    product_number = models.FloatField(verbose_name='产品数量', default=0)
