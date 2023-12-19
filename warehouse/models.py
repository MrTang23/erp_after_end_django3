from django.db import models


# Create your models here.
# 材料表
class RawMaterial(models.Model):
    material_id = models.AutoField(verbose_name='材料id', primary_key=True)
    material_name = models.CharField(verbose_name='材料名', max_length=32)
    material_type = models.CharField(verbose_name='材料型号', max_length=32, default='6414型')
    material_color = models.CharField(verbose_name='颜色', max_length=10, default='颜色')
    material_supplier = models.CharField(verbose_name='供应商名称', max_length=32, default='供应商')
    material_product_supplier = models.CharField(verbose_name='生产厂商名称', max_length=32, default='生产厂商')
    material_weight = models.FloatField(verbose_name='原料重量', default=0)
    recycle_material_weight = models.FloatField(verbose_name="水口料重量", default=0)
    shelf_number = models.CharField(verbose_name='货架编号', default='无',max_length=10)
    remark = models.CharField(verbose_name='备注', max_length=50, default='无备注')

    class Meta:
        unique_together = (
            'material_name', 'material_type', 'material_color', 'material_supplier', 'material_product_supplier')


# 生产领取材料表
class MaterialGetNormal(models.Model):
    material_get_id = models.AutoField(verbose_name='材料领取id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id', default=3)
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32, default='未填写')
    production_order_id = models.CharField(verbose_name='生产指令单id', max_length=32)
    factory_manager_confirm = models.IntegerField(verbose_name='厂长确认', default=0)
    material_get_img = models.CharField(verbose_name='材料领取单', max_length=32)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    factory_manager_confirm_time = models.CharField(verbose_name='厂长确认时间', max_length=32,
                                                    default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 连接材料领取表
class LinkMaterialGetNormal(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_get_id = models.IntegerField(verbose_name='材料领取id', default=0)
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_weight = models.FloatField(verbose_name='材料领取重量')


# 材料采购表
class MaterialPurchase(models.Model):
    material_purchase_id = models.AutoField(verbose_name='原料采购单id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id')
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32)
    delivery_note_img = models.CharField(verbose_name='送货单', max_length=32)
    warehousing_entry_img = models.CharField(verbose_name='入库单', max_length=32, default='empty')
    quality_confirm = models.IntegerField(verbose_name='品控确认', default=0)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    quality_confirm_time = models.CharField(verbose_name='品控确认时间', max_length=32, default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 材料采购连接材料名表
class LinkMaterialPurchase(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_purchase_id = models.IntegerField(verbose_name='原料采购单据id')
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_from = models.CharField(verbose_name='材料来源', max_length=8, default='采购')
    material_purchase_weight = models.FloatField(verbose_name='原料购买重量')


# 材料退库表
class MaterialBack(models.Model):
    material_back_id = models.AutoField(verbose_name='材料退库单id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id')
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32)
    # 指令单状态：1:正常 0:暂停 -1:已完结
    production_order_status = models.IntegerField(verbose_name='指令单状态', default=1)
    back_warehouse_img = models.CharField(verbose_name='退库单', max_length=32)
    factory_manager_confirm = models.IntegerField(verbose_name='厂长确认', default=0)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    factory_manager_confirm_time = models.CharField(verbose_name='厂长确认时间', max_length=32,
                                                    default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 材料退库连接材料表名
class LinkMaterialBack(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_back_id = models.IntegerField(verbose_name='原料退库单据id')
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_back_kind = models.IntegerField(verbose_name='材料退库种类')
    material_back_weight = models.FloatField(verbose_name='材料退库重量')
    back_remark = models.CharField(verbose_name='备注', max_length=50, default='无备注')


# 材料出厂
class MaterialOutFactory(models.Model):
    material_out_factory_id = models.AutoField(verbose_name='材料出厂单id', primary_key=True)
    apply_user_id = models.IntegerField(verbose_name='申请人id')
    create_time = models.CharField(verbose_name='申请创建时间', max_length=32)
    material_out_factory_img = models.CharField(verbose_name='材料出厂单', max_length=32)
    deputy_manager_confirm = models.IntegerField(verbose_name='副总确认', default=0)
    general_manager_confirm = models.IntegerField(verbose_name='总经理确认', default=2)
    warehousing_confirm = models.IntegerField(verbose_name='仓库确认', default=2)
    deputy_manager_confirm_time = models.CharField(verbose_name='副总经理确认时间', max_length=32,
                                                           default='yyyy-mm-dd hh:mm:ss')
    general_manager_confirm_time = models.CharField(verbose_name='总经理确认时间', max_length=32,
                                                    default='yyyy-mm-dd hh:mm:ss')
    warehousing_confirm_time = models.CharField(verbose_name='仓库确认时间', max_length=32,
                                                default='yyyy-mm-dd hh:mm:ss')


# 材料出厂连接材料表名
class LinkMaterialOutFactory(models.Model):
    index = models.AutoField(verbose_name='序号', primary_key=True)
    material_out_factory_id = models.IntegerField(verbose_name='材料出厂单id')
    material_id = models.IntegerField(verbose_name='材料id', default=0)
    material_kind = models.IntegerField(verbose_name='材料种类')
    material_weight = models.FloatField(verbose_name='材料出厂重量')
    remark = models.CharField(verbose_name='备注', max_length=10)
