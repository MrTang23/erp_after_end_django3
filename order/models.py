from django.db import models


# Create your models here.
# 生产指令基本表
class ProductionOrder(models.Model):
    production_order_id = models.CharField(verbose_name='生产指令单编号', primary_key=True, max_length=32)
    apply_user_id = models.IntegerField(verbose_name='申请人id')
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32)
    custom = models.CharField(verbose_name='客户', max_length=10, default='无')
    custom_deadline = models.CharField(verbose_name='客户交期', max_length=12, default='9999-99-99')
    mould_name = models.CharField(verbose_name='磨具编号', max_length=64)
    molding_cycle = models.CharField(verbose_name='成型周期', max_length=32)
    # 指令单状态：1:正常 0:暂停 -1:已完结
    production_order_status = models.IntegerField(verbose_name='指令单状态', default=1)
    production_order_img = models.CharField(verbose_name='内部生产指令单', max_length=32)
    quality_confirm = models.IntegerField(verbose_name='品控确认', default=0)
    factory_manager_confirm = models.IntegerField(verbose_name='厂长确认', default=2)
    quality_confirm_time = models.CharField(verbose_name='品控确认时间', max_length=32, default='yyyy-mm-dd hh:mm:ss')
    factory_manager_confirm_time = models.CharField(verbose_name='厂长确认时间', max_length=32,
                                                    default='yyyy-mm-dd hh:mm:ss')


# 生产指令连接原料表
class LinkProductionOrderByMaterial(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    production_order_id = models.CharField(verbose_name='生产指令单据id', max_length=32)
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_order_kind = models.IntegerField(verbose_name='材料种类')
    material_order_weight = models.FloatField(verbose_name='材料重量')
    material_used_weight = models.FloatField(verbose_name='已领取材料重量', default=0)


# 生产指令连接产品表
class LinkProductionOrderByProduct(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    production_order_id = models.CharField(verbose_name='生产指令单据id', max_length=32)
    product_name = models.CharField(verbose_name='产品名', max_length=32)
    # 1:是半成品 0:不是半成品
    if_semi_finished = models.IntegerField(verbose_name='是否半成品', default=0)
    product_number = models.IntegerField(verbose_name='订单产品数量')
    product_weight = models.FloatField(verbose_name='产品净重')
    product_received_number = models.IntegerField(verbose_name='产品已入库数量', default=0)
    product_second_shipped_number = models.IntegerField(verbose_name='产品重工出库数量', default=0)
    product_second_received_number = models.IntegerField(verbose_name='产品重工入库数量', default=0)
    product_shipped_number = models.IntegerField(verbose_name='产品已出货数量', default=0)


# 试料基本表
class MaterialTestOrder(models.Model):
    material_test_order_id = models.CharField(verbose_name='试料单编号', primary_key=True, max_length=32)
    apply_user_id = models.IntegerField(verbose_name='申请人id')
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32)
    custom = models.CharField(verbose_name='客户', max_length=10, default='无')
    mould_name = models.CharField(verbose_name='磨具编号', max_length=64)
    machine_name = models.CharField(verbose_name='机种名', max_length=64)
    material_test_order_img = models.CharField(verbose_name='试料指令单', max_length=32)
    deputy_manager_confirm = models.IntegerField(verbose_name='副总确认', default=0)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    deputy_manager_confirm_time = models.CharField(verbose_name='副总确认时间', max_length=32,
                                                           default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')
    test_reason = models.CharField(verbose_name='试料原因', max_length=100)


# 试料连接原料表
class LinkMaterialTestByMaterial(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_test_order_id = models.CharField(verbose_name='试料单据id', max_length=32)
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_order_kind = models.IntegerField(verbose_name='材料种类')
    material_order_weight = models.FloatField(verbose_name='材料重量')


# 生产指令连接产品表
class LinkMaterialTestByProduct(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_test_order_id = models.CharField(verbose_name='试料单据id', max_length=32)
    product_name = models.CharField(verbose_name='产品名', max_length=32)
    # 1:是半成品 0:不是半成品
    if_semi_finished = models.IntegerField(verbose_name='是否半成品', default=0)
    product_number = models.IntegerField(verbose_name='订单产品数量')


