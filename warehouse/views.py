import json

from django.http import JsonResponse
from warehouse import models as warehouse_models
from order import models as order_models


def test_function(request):
    body = json.loads(request.body)
    a = body.get('a')
    b = body.get('b')
    c = a * b
    res = {
        'code': 1,
        'data': c,
        'msg': '运算成功'
    }
    return JsonResponse(res)


# 添加材料
def add_new_material(request):
    body = json.loads(request.body)
    if warehouse_models.RawMaterial.objects.filter(material_name=body.get('new_material_name'),
                                                   material_type=body.get('new_material_type'),
                                                   material_supplier=body.get('new_material_supplier'),
                                                   material_product_supplier=body.get('new_material_product_supplier')):
        res = {
            'code': 0,
            'msg': '该产品已存在，请勿重复添加'
        }
        return JsonResponse(res)
    else:
        warehouse_models.RawMaterial.objects.create(material_name=body.get('new_material_name'),
                                                    material_type=body.get('new_material_type'),
                                                    material_supplier=body.get('new_material_supplier'),
                                                    material_product_supplier=body.get('new_material_product_supplier'))
        res = {
            'code': 1,
            'msg': '新增材料成功'
        }
        return JsonResponse(res)


# 生产领材料
def material_get_normal(request):
    body = json.loads(request.body)
    # 判断指令单是否存在以及指令单状态
    if order_models.ProductionOrder.objects.filter(
            production_order_id=body.get('production_order_id')) and order_models.ProductionOrder.objects.filter(
        production_order_status=1):

        # 写入生产领材料基本表
        warehouse_models.MaterialGetNormal.objects.create(apply_user_id=body.get('user_id'),
                                                          create_time=body.get('create_time'),
                                                          production_order_id=body.get('production_order_id'),
                                                          material_get_img=body.get('material_get_img'))

        # 获取新增的基本表数据的id以及需要领取的材料列表
        material_get_list = warehouse_models.MaterialGetNormal.objects.filter(
            create_time=body.get('create_time')).first()
        material_get_id = material_get_list.material_get_id
        material_list = body.get('material_list')
        # 循环便利需要入库的列表
        for item in material_list:

            # 判断该材料id是否存在
            if warehouse_models.RawMaterial.objects.filter(material_id=item.get('material_id')):
                # 获取领取材料的种类 0:原料 1:水口料
                material_kind_queryset = order_models.LinkProductionOrderByMaterial.objects.filter(
                    production_order_id=body.get('production_order_id')).first()
                material_kind = material_kind_queryset.material_order_kind
                # 获取材料库存基本表中对应材料种类的重量
                stock_material_weight_queryset = warehouse_models.RawMaterial.objects.filter(
                    material_id=item.get('material_id')).first()
                if material_kind == 0:
                    row_material_weight = stock_material_weight_queryset.material_weight
                else:
                    row_material_weight = stock_material_weight_queryset.recycle_material_weight

                # 判断是否领用超出库存
                if item.get('material_weight') <= row_material_weight:

                    # 判断是否超出该订单对应原料可领取数量
                    production_order_weight_queryset = order_models.LinkProductionOrderByMaterial.objects.filter(
                        production_order_id=body.get('production_order_id'), material_order_kind=material_kind).first()
                    production_order_used_weight_queryset = order_models.LinkProductionOrderByMaterial.objects.filter(
                        production_order_id=body.get('production_order_id'), material_order_kind=material_kind).first()
                    can_get_weight = (production_order_weight_queryset.material_order_weight -
                                      production_order_used_weight_queryset.material_used_weight)
                    if can_get_weight > 0 and item.get('material_weight') <= can_get_weight:
                        warehouse_models.LinkMaterialGetNormal.objects.create(material_id=item.get('material_id'),
                                                                              material_get_id=material_get_id,
                                                                              material_weight=item.get(
                                                                                  'material_weight'))
                    else:
                        warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).delete()
                        res = {
                            'code': 0,
                            'data': '',
                            'msg': '无法领取，请填写超领单'
                        }
                        return JsonResponse(res)
                else:
                    warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).delete()
                    res = {
                        'code': 0,
                        'data': '',
                        'msg': '材料库存不足'
                    }
                    return JsonResponse(res)
            else:
                # 删除基本表刚写入数据
                warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).delete()
                res = {
                    'code': 0,
                    'data': '',
                    'msg': '材料不存在'
                }
                return JsonResponse(res)
        res = {
            'code': 1,
            'data': '',
            'msg': '材料领取成功'
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'data': '',
            'msg': '指令单不存在或指令单未激活'
        }
        return JsonResponse(res)


# 提交材料出厂表单
def material_out_factory(request):
    body = json.loads(request.body)
    if body.get('role_id') == 5:
        # 写入采购表
        warehouse_models.MaterialOutFactory.objects.create(apply_user_id=body.get('user_id'),
                                                           create_time=body.get('create_time'),
                                                           material_out_factory_img=body.get(
                                                               'material_out_factory_img'))
        out_list = warehouse_models.MaterialOutFactory.objects.filter(create_time=body.get('create_time')).first()
        out_id = out_list.material_out_factory_id
        material_list = body.get('material_list')
        # 更新连接表
        for material_item in material_list:
            if warehouse_models.RawMaterial.objects.filter(material_id=material_item.get('material_id')):
                # 获取该原料所在行数据
                material_stock = warehouse_models.RawMaterial.objects.filter(
                    material_id=material_item.get('material_id')).first()
                # 判断是否超出库存量
                # material_kind 0:原料 1:水口料
                if material_item.get('material_kind') == 0:
                    if material_stock.material_weight < material_item.get('material_weight'):
                        res = {
                            'code': 0,
                            'msg': "材料库存不足，无法出厂"
                        }
                        return JsonResponse(res)
                if material_item.get('material_kind') == 1:
                    if material_stock.recycle_material_weight < material_item.get('material_weight'):
                        res = {
                            'code': 0,
                            'msg': "材料库存不足，无法出厂"
                        }
                        return JsonResponse(res)
                # 写入数据库
                warehouse_models.LinkMaterialOutFactory.objects.create(material_out_factory_id=out_id,
                                                                       material_id=material_item.get('material_id'),
                                                                       material_weight=material_item.get(
                                                                           'material_weight'),
                                                                       material_kind=material_item.get(
                                                                           'material_kind'),
                                                                       remark=material_item.get(
                                                                           'remark')
                                                                       )
                res = {
                    'code': 1,
                    'msg': "申请材料出厂成功"
                }
            else:
                warehouse_models.MaterialOutFactory.objects.filter(material_back_id=out_id).delete()
                res = {
                    'code': 0,
                    'msg': "原料名称错误"
                }
                return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'msg': "权限不足"
        }
        return JsonResponse(res)
    return JsonResponse(res)


# 提交材料退库表单
def material_back(request):
    body = json.loads(request.body)
    if body.get('role_id') == 7:
        # 写入退库表
        warehouse_models.MaterialBack.objects.create(apply_user_id=body.get('user_id'),
                                                     create_time=body.get('create_time'),
                                                     back_warehouse_img=body.get('back_warehouse_img'))
        back_list = warehouse_models.MaterialBack.objects.filter(create_time=body.get('create_time')).first()
        back_id = back_list.material_back_id
        material_list = body.get('material_list')
        # 更新连接表
        for material_item in material_list:
            if warehouse_models.RawMaterial.objects.filter(material_id=material_item.get('material_id')):
                # material_back_kind 0:原料 1:水口料
                warehouse_models.LinkMaterialBack.objects.create(material_back_id=back_id,
                                                                 material_id=material_item.get('material_id'),
                                                                 material_back_weight=material_item.get(
                                                                     'material_weight'),
                                                                 material_back_kind=material_item.get(
                                                                     'material_back_kind'),
                                                                 back_remark=material_item.get(
                                                                     'back_remark')
                                                                 )
            else:
                warehouse_models.MaterialBack.objects.filter(material_back_id=back_id).delete()
                res = {
                    'code': 0,
                    'msg': "原料名称错误"
                }
                return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'msg': "权限不足"
        }
        return JsonResponse(res)
    res = {
        'code': 1,
        'msg': "申请材料库退成功"
    }
    return JsonResponse(res)


# 获取材料库存
def get_material_stock(request):
    data_array = []
    for item in warehouse_models.RawMaterial.objects.all():
        stock_obj = {
            'material_id': item.material_id,
            'material_name': item.material_name,
            'material_supplier': item.material_supplier,
            'material_type': item.material_type,
            'material_product_supplier': item.material_product_supplier,
            'material_weight': item.material_weight,
            'recycle_material_weight': item.recycle_material_weight,
            'remark': item.remark,
            'shelf_number': item.shelf_number,
            'material_color': item.material_color
        }
        data_array.append(stock_obj)
    res = {
        'code': 1,
        'data': data_array,
        'msg': "获取材料库存成功"
    }
    return JsonResponse(res)


# 提交原料采购表单
def material_purchase(request):
    body = json.loads(request.body)
    if body.get('role_id') == 5:
        # 写入采购表
        warehouse_models.MaterialPurchase.objects.create(apply_user_id=body.get('user_id'),
                                                         create_time=body.get('create_time'),
                                                         delivery_note_img=body.get('delivery_note_img'))
        purchase_list = warehouse_models.MaterialPurchase.objects.filter(create_time=body.get('create_time')).first()
        purchase_id = purchase_list.material_purchase_id
        material_list = body.get('material_list')
        # 更新连接表
        for material_item in material_list:
            if warehouse_models.RawMaterial.objects.filter(material_id=material_item.get('material_id')):
                warehouse_models.LinkMaterialPurchase.objects.create(material_purchase_id=purchase_id,
                                                                     material_id=material_item.get('material_id'),
                                                                     material_purchase_weight=material_item.get(
                                                                         'material_weight'),

                                                                     material_from=material_item.get(
                                                                         'material_from')
                                                                     )
                # # 将入库重量加到材料表
                # material_total_weight = material_item.get(
                #     'material_weight') + warehouse_models.RawMaterial.objects.filter(
                #     material_name=material_item.get('material_name')).first().material_weight
                # warehouse_models.RawMaterial.objects.filter(
                #     material_name=material_item.get('material_name')).update(
                #     material_weight='%.2f' % material_total_weight)
                res = {
                    'code': 1,
                    'msg': "申请原料入库成功"
                }
            else:
                warehouse_models.MaterialPurchase.objects.filter(material_purchase_id=purchase_id).delete()
                res = {
                    'code': 0,
                    'msg': "原料名称错误"
                }
    else:
        res = {
            'code': 0,
            'msg': "权限不足"
        }
    return JsonResponse(res)


# 获取所有材料名
def get_all_material_name(request):
    material_name_list = list(warehouse_models.RawMaterial.objects.values_list('material_id', flat=True))

    select_list = []
    for item in material_name_list:
        row_data = warehouse_models.RawMaterial.objects.filter(material_id=item).first()
        temp_obj = {
            'label': row_data.material_name + ' ' + row_data.material_type + ' ' + row_data.material_color + ' ' +
                     row_data.material_product_supplier + ' ' + row_data.material_supplier + ' ' + row_data.remark,
            'value': item
        }
        select_list.append(temp_obj)
    res = {
        'code': 1,
        'data': select_list,
        'msg': "获取材料名列表成功"
    }
    return JsonResponse(res)


# 根据id获取材料名
def get_material_name_by_id(request):
    body = json.loads(request.body)
    queryset = warehouse_models.RawMaterial.objects.filter(material_id=body.get('material_id')).first()
    material_name = (queryset.material_name + ' ' + queryset.material_type + ' ' + queryset.material_color + ' ' +
                     queryset.material_product_supplier + ' ' + queryset.material_supplier + ' ' + queryset.remark)
    res = {
        'code': 1,
        'data': material_name,
        'msg': "获取材料名成功"
    }
    return JsonResponse(res)
