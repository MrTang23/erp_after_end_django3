import json
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from warehouse import models as warehouse_models
from order import models as order_models
from product import models as product_models
from login import models as login_models


# Create your views here.
# 获取当前时间
def get_time(request):
    current_time = datetime.now()
    month = str(current_time.month)
    day = str(current_time.day)
    hour = str(current_time.hour)
    minute = str(current_time.minute)
    second = str(current_time.second)

    if current_time.month < 10:
        month = '0' + str(current_time.month)
    if current_time.day < 10:
        day = '0' + str(current_time.day)
    if current_time.hour < 10:
        hour = '0' + str(current_time.hour)
    if current_time.minute < 10:
        minute = '0' + str(current_time.minute)
    if current_time.second < 10:
        second = '0' + str(current_time.second)
    return str(current_time.year) + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second


# 创建生产指令单
def make_production_order(request):
    body = json.loads(request.body)
    if body.get('role_id') == 5:
        # 写入生产指令单表
        order_models.ProductionOrder.objects.create(apply_user_id=body.get('user_id'),
                                                    create_time=body.get('create_time'),
                                                    production_order_id=body.get('production_order_id'),
                                                    custom=body.get('custom'),
                                                    custom_deadline=body.get('custom_deadline'),
                                                    mould_name=body.get('mould_name'),
                                                    molding_cycle=body.get('molding_cycle'),
                                                    production_order_img=body.get('production_order_img')
                                                    )
        material_list = body.get('material_list')
        production_list = body.get('production_list')
        # 更新材料连接表
        for material_item in material_list:
            if warehouse_models.RawMaterial.objects.filter(material_id=material_item.get('material_id')):
                order_models.LinkProductionOrderByMaterial.objects.create(
                    production_order_id=body.get('production_order_id'),
                    material_id=material_item.get(
                        'material_id'),
                    material_order_weight=material_item.get(
                        'material_order_weight'),
                    material_order_kind=material_item.get(
                        'material_order_kind')

                )
            else:
                order_models.ProductionOrder.objects.filter(
                    production_order_id=body.get('production_order_id')).delete()
                res = {
                    'code': 0,
                    'msg': "原料名称错误"
                }
                return JsonResponse(res)
        # 更新产品连接表
        for product_item in production_list:
            if product_models.Product.objects.filter(product_name=product_item.get('product_name')):
                order_models.LinkProductionOrderByProduct.objects.create(
                    production_order_id=body.get('production_order_id'),
                    product_name=product_item.get(
                        'product_name'),
                    product_weight=product_item.get(
                        'product_weight'),
                    product_number=product_item.get(
                        'product_number'),
                    if_semi_finished=product_item.get('if_semi_finished')
                )
            else:
                order_models.ProductionOrder.objects.filter(
                    production_order_id=body.get('production_order_id')).delete()
                order_models.LinkProductionOrderByMaterial.objects.filter(
                    production_order_id=body.get('production_order_id')).delete()
                res = {
                    'code': 0,
                    'msg': "产品名称错误"
                }
                return JsonResponse(res)
        res = {
            'code': 1,
            'msg': "生产指令单创建成功"
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'msg': "权限不足"
        }
        return JsonResponse(res)


# 获取审批弹窗的数据
def get_approval_dialog_data(request):
    body = json.loads(request.body)
    if body.get('form_name') == '生产指令单申请':
        production_order_id = body.get('form_id')
        production_order_queryset = order_models.ProductionOrder.objects.filter(
            production_order_id=production_order_id).first()
        production_order_material_list_all = order_models.LinkProductionOrderByMaterial.objects.filter(
            production_order_id=production_order_id)
        material_list = []
        for production_order_material_list in production_order_material_list_all:
            material_id = production_order_material_list.material_id
            row_data = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()

            material_kind = production_order_material_list.material_order_kind
            if material_kind == 0:
                material_kind = '原料'
            else:
                material_kind = '水口料'
            material_order_weight = production_order_material_list.material_order_weight
            temp_obj = {
                'material_id': material_id,
                'material_name': row_data.material_name,
                'material_type': row_data.material_type,
                'material_kind': material_kind,
                'material_color': row_data.material_color,
                'material_product_supplier': row_data.material_product_supplier,
                'material_supplier': row_data.material_supplier,
                'remark': row_data.remark,
                'material_weight': material_order_weight
            },
            material_list.append(temp_obj[0])
        production_order_product_list_all = order_models.LinkProductionOrderByProduct.objects.filter(
            production_order_id=production_order_id)
        product_list = []
        for production_order_product_list in production_order_product_list_all:
            product_name = production_order_product_list.product_name
            product_kind = production_order_product_list.if_semi_finished
            if product_kind == 0:
                product_kind = '成品'
            else:
                product_kind = '半成品'
            product_number = production_order_product_list.product_number
            product_weight = production_order_product_list.product_weight
            temp_obj = {
                'product_name': product_name,
                'product_kind': product_kind,
                'product_number': product_number,
                'product_weight': product_weight
            },
            product_list.append(temp_obj[0])
        res = {
            'code': 1,
            'data': {
                'form_name': '生产指令单申请',
                'create_time': production_order_queryset.create_time,
                'production_order_img': settings.IMAGE + '/' + production_order_queryset.production_order_img,
                'production_order_id': production_order_id,
                'custom': production_order_queryset.custom,
                'mould_name': production_order_queryset.mould_name,
                'molding_cycle': production_order_queryset.molding_cycle,
                'material_list': material_list,
                'product_list': product_list
            },
            'msg': "获取指令单审批内容成功"
        }
        return JsonResponse(res)
    if body.get('form_name') == '材料领取申请':
        material_get_id = int(body.get('form_id'))

        material_get_normal_queryset = warehouse_models.MaterialGetNormal.objects.filter(
            material_get_id=material_get_id).first()
        production_order_id = material_get_normal_queryset.production_order_id

        material_list_all = warehouse_models.LinkMaterialGetNormal.objects.filter(
            material_get_id=material_get_id)
        material_list = []
        for item in material_list_all:
            material_id = item.material_id
            row_data = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()
            material_queryset = order_models.LinkProductionOrderByMaterial.objects.filter(
                production_order_id=production_order_id,
                material_id=material_id).first()
            material_kind = material_queryset.material_order_kind
            if material_kind == 0:
                material_kind = '原料'
            else:
                material_kind = '水口料'
            temp_obj = {
                'material_id': material_id,
                'material_name': row_data.material_name,
                'material_type': row_data.material_type,
                'material_kind': material_kind,
                'material_color': row_data.material_color,
                'material_product_supplier': row_data.material_product_supplier,
                'material_supplier': row_data.material_supplier,
                'remark': row_data.remark,
                'material_weight': item.material_weight
            },
            material_list.append(temp_obj[0])
        res = {
            'code': 1,
            'data': {
                'form_name': '材料领取申请',
                'material_get_id': material_get_id,
                'create_time': material_get_normal_queryset.create_time,
                'material_get_img': settings.IMAGE + '/' + material_get_normal_queryset.material_get_img,
                'production_order_id': production_order_id,
                'material_list': material_list
            },
            'msg': "获取材料入库内容成功"
        }
        return JsonResponse(res)
    if body.get('form_name') == '产品入库申请':
        product_storage_id = int(body.get('form_id'))
        product_storage_queryset = product_models.ProductStorageNormal.objects.filter(
            product_storage_id=product_storage_id).first()
        link_product_storage_queryset = product_models.LinkProductStorageNormal.objects.filter(
            product_storage_id=product_storage_id)
        product_list = []
        for item in link_product_storage_queryset:
            production_order_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                production_order_id=product_storage_queryset.production_order_id,
                product_name=item.product_name).first()
            product_kind = production_order_queryset.if_semi_finished
            if product_kind == 0:
                product_kind = '成品'
            else:
                product_kind = '半成品'
            temp_obj = {
                'product_name': item.product_name,
                'product_number': item.product_number,
                'product_kind': product_kind
            }
            product_list.append(temp_obj)
        res = {
            'code': 1,
            'data': {
                'form_name': '产品入库申请',
                'product_storage_id': product_storage_id,
                'create_time': product_storage_queryset.create_time,
                'product_storage_img': settings.IMAGE + '/' + product_storage_queryset.product_storage_img,
                'production_order_id': product_storage_queryset.production_order_id,
                'product_list': product_list
            },
            'msg': "获取指令单审批内容成功"
        }
        return JsonResponse(res)
    if body.get('form_name') == '材料入库申请':
        material_purchase_id = int(body.get('form_id'))

        material_get_normal_queryset = warehouse_models.MaterialPurchase.objects.filter(
            material_purchase_id=material_purchase_id).first()

        material_list_all = warehouse_models.LinkMaterialPurchase.objects.filter(
            material_purchase_id=material_purchase_id)
        material_list = []
        for item in material_list_all:
            material_id = item.material_id
            row_data = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()

            temp_obj = {
                'material_id': material_id,
                'material_name': row_data.material_name,
                'material_type': row_data.material_type,
                'material_kind': '原料',
                'material_color': row_data.material_color,
                'material_product_supplier': row_data.material_product_supplier,
                'material_supplier': row_data.material_supplier,
                'remark': row_data.remark,
                'material_weight': item.material_purchase_weight,
                'material_from': item.material_from
            },
            material_list.append(temp_obj[0])
        res = {
            'code': 1,
            'data': {
                'form_name': '材料入库申请',
                'material_purchase_id': material_purchase_id,
                'create_time': material_get_normal_queryset.create_time,
                'material_purchase_img': settings.IMAGE + '/' + material_get_normal_queryset.delivery_note_img,
                'material_list': material_list
            },
            'msg': "获取材料入库内容成功"
        }
        return JsonResponse(res)
    if body.get('form_name') == '产品出货申请':
        product_shipment_id = int(body.get('form_id'))
        product_shipment_queryset = product_models.ProductShipmentNormal.objects.filter(
            product_shipment_id=product_shipment_id).first()
        link_product_shipment_queryset = product_models.LinkProductShipmentNormal.objects.filter(
            product_shipment_id=product_shipment_id)
        product_list = []
        for item in link_product_shipment_queryset:
            production_order_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                production_order_id=product_shipment_queryset.production_order_id,
                product_name=item.product_name).first()
            product_kind = production_order_queryset.if_semi_finished
            if product_kind == 0:
                product_kind = '成品'
            else:
                product_kind = '半成品'
            temp_obj = {
                'product_name': item.product_name,
                'product_number': item.product_number,
                'product_kind': product_kind
            }
            product_list.append(temp_obj)
        res = {
            'code': 1,
            'data': {
                'form_name': '产品出货申请',
                'product_shipment_id': product_shipment_id,
                'create_time': product_shipment_queryset.create_time,
                'product_shipment_img': settings.IMAGE + '/' + product_shipment_queryset.product_shipment_img,
                'production_order_id': product_shipment_queryset.production_order_id,
                'product_list': product_list
            },
            'msg': "获取产品出货内容成功"
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'msg': "未查询到该申请"
        }
        return JsonResponse(res)


# 处理审批结果
def handel_approval_result(request):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    status = body.get('status')
    if body.get('form_name') == '生产指令单申请':
        production_order_id = body.get('id')
        if user_id == 4:
            if status == 1:
                order_models.ProductionOrder.objects.filter(production_order_id=production_order_id).update(
                    quality_confirm=1, factory_manager_confirm=0, quality_confirm_time=get_time(request))
            else:
                order_models.ProductionOrder.objects.filter(production_order_id=production_order_id).update(
                    quality_confirm=-1, quality_confirm_time=get_time(request))
        if user_id == 7:
            if status == 1:
                order_models.ProductionOrder.objects.filter(production_order_id=production_order_id).update(
                    factory_manager_confirm=1, factory_manager_confirm_time=get_time(request))
            else:
                order_models.ProductionOrder.objects.filter(production_order_id=production_order_id).update(
                    factory_manager_confirm=-1, factory_manager_confirm_time=get_time(request))
        res = {
            'code': 1,
            'msg': "处理生产指令单成功"
        }
        return JsonResponse(res)
    elif body.get('form_name') == '材料领取申请':
        material_get_id = body.get('id')
        if user_id == 7:
            if status == 1:
                warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).update(
                    factory_manager_confirm=1, warehousing_confirm=0, factory_manager_confirm_time=get_time(request))
            else:
                warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).update(
                    factory_manager_confirm=-1, factory_manager_confirm_time=get_time(request))
        if user_id == 6:
            if status == 1:
                warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).update(
                    warehousing_confirm=1, warehousing_confirm_time=get_time(request))
                material_get_queryset = warehouse_models.MaterialGetNormal.objects.filter(
                    material_get_id=material_get_id).first()
                production_order_id = material_get_queryset.production_order_id
                material_get_list = warehouse_models.LinkMaterialGetNormal.objects.filter(
                    material_get_id=material_get_id)
                for item in material_get_list:
                    material_id = item.material_id
                    production_order_queryset = order_models.LinkProductionOrderByMaterial.objects.filter(
                        production_order_id=production_order_id, material_id=material_id).first()
                    material_used_weight = production_order_queryset.material_used_weight
                    material_get_weight = item.material_weight
                    material_update_used_weight = material_used_weight + material_get_weight
                    order_models.LinkProductionOrderByMaterial.objects.filter(production_order_id=production_order_id,
                                                                              material_id=material_id).update(
                        material_used_weight=material_update_used_weight)
                    material_kind = production_order_queryset.material_order_kind
                    material_queryset = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()
                    if material_kind == 0:
                        warehouse_models.RawMaterial.objects.filter(material_id=material_id).update(
                            material_weight=material_queryset.material_weight - material_get_weight)
                    else:
                        warehouse_models.RawMaterial.objects.filter(material_id=material_id).update(
                            recycle_material_weight=material_queryset.recycle_material_weight - material_get_weight)

            else:
                warehouse_models.MaterialGetNormal.objects.filter(material_get_id=material_get_id).update(
                    warehousing_confirm=-1, warehousing_confirm_time=get_time(request))
        res = {
            'code': 1,
            'msg': "处理生产领料成功"
        }
        return JsonResponse(res)
    elif body.get('form_name') == '产品入库申请':
        product_storage_id = body.get('id')
        if user_id == 4:
            if status == 1:
                product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).update(
                    quality_confirm=1, warehousing_confirm=0, quality_confirm_time=get_time(request))
            else:
                product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).update(
                    quality_confirm=-1, quality_confirm_time=get_time(request))
        if user_id == 6:
            if status == 1:
                product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).update(
                    warehousing_confirm=1, warehousing_confirm_time=get_time(request))
                link_product_storage_queryset = product_models.LinkProductStorageNormal.objects.filter(
                    product_storage_id=product_storage_id)
                product_storage_queryset = product_models.ProductStorageNormal.objects.filter(
                    product_storage_id=product_storage_id).first()
                production_order_id = product_storage_queryset.production_order_id
                for item in link_product_storage_queryset:
                    product_kind_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                        production_order_id=production_order_id, product_name=item.product_name).first()
                    product_kind = product_kind_queryset.if_semi_finished
                    product_received_number = product_kind_queryset.product_received_number
                    product_received_number = product_received_number + item.product_number
                    order_models.LinkProductionOrderByProduct.objects.filter(production_order_id=production_order_id,
                                                                             product_name=item.product_name).update(
                        product_received_number=product_received_number)
                    product_queryset = product_models.Product.objects.filter(product_name=item.product_name).first()
                    if product_kind == 0:
                        product_number = product_queryset.product_number + item.product_number
                        product_models.Product.objects.filter(product_name=item.product_name).update(
                            product_number=product_number)
                    else:
                        product_number = product_queryset.product_semi_finished_number + item.product_number
                        print(product_number)
                        product_models.Product.objects.filter(product_name=item.product_name).update(
                            product_semi_finished_number=product_number)
            else:
                product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).update(
                    warehousing_confirm=-1, warehousing_confirm_time=get_time(request))
        res = {
            'code': 1,
            'msg': "处理生产领料成功"
        }
        return JsonResponse(res)
    elif body.get('form_name') == '材料入库申请':
        material_purchase_id = body.get('id')
        if user_id == 4:
            if status == 1:
                warehouse_models.MaterialPurchase.objects.filter(material_purchase_id=material_purchase_id).update(
                    quality_confirm=1, warehousing_confirm=0, quality_confirm_time=get_time(request))
            else:
                warehouse_models.MaterialPurchase.objects.filter(material_purchase_id=material_purchase_id).update(
                    quality_confirm=-1, quality_confirm_time=get_time(request))
        if user_id == 6:
            if status == 1:
                warehouse_models.MaterialPurchase.objects.filter(material_purchase_id=material_purchase_id).update(
                    warehousing_confirm=1, warehousing_confirm_time=get_time(request))
                material_get_list = warehouse_models.LinkMaterialPurchase.objects.filter(
                    material_purchase_id=material_purchase_id)
                for item in material_get_list:
                    material_id = item.material_id
                    material_purchase_weight = item.material_purchase_weight
                    material_queryset = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()
                    material_weight = material_queryset.material_weight + material_purchase_weight
                    warehouse_models.RawMaterial.objects.filter(material_id=material_id).update(
                        material_weight=material_weight)
            else:
                warehouse_models.MaterialPurchase.objects.filter(material_purchase_id=material_purchase_id).update(
                    warehousing_confirm=-1, warehousing_confirm_time=get_time(request))
        res = {
            'code': 1,
            'msg': "处理生产领料成功"
        }
        return JsonResponse(res)
    elif body.get('form_name') == '产品出货申请':
        product_shipment_id = body.get('id')
        if user_id == 4:
            if status == 1:
                product_models.ProductShipmentNormal.objects.filter(product_shipment_id=product_shipment_id).update(
                    quality_confirm=1, warehousing_confirm=0, quality_confirm_time=get_time(request))
                print(product_shipment_id,body)
            else:
                product_models.ProductShipmentNormal.objects.filter(product_shipment_id=product_shipment_id).update(
                    quality_confirm=-1, quality_confirm_time=get_time(request))
        if user_id == 6:
            if status == 1:
                product_models.ProductShipmentNormal.objects.filter(product_shipment_id=product_shipment_id).update(
                    warehousing_confirm=1, warehousing_confirm_time=get_time(request))
                link_product_shipment_queryset = product_models.LinkProductShipmentNormal.objects.filter(
                    product_shipment_id=product_shipment_id)
                product_shipment_queryset = product_models.ProductShipmentNormal.objects.filter(
                    product_shipment_id=product_shipment_id).first()
                production_order_id = product_shipment_queryset.production_order_id
                for item in link_product_shipment_queryset:
                    product_kind_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                        production_order_id=production_order_id, product_name=item.product_name).first()
                    product_kind = product_kind_queryset.if_semi_finished
                    product_shipped_number = product_kind_queryset.product_shipped_number
                    product_shipped_number = product_shipped_number + item.product_number
                    if product_shipped_number >= product_kind_queryset.product_number:
                        res = {
                            'code': 0,
                            'msg': "已超出可出货数量"
                        }
                        return JsonResponse(res)
                    order_models.LinkProductionOrderByProduct.objects.filter(production_order_id=production_order_id,
                                                                             product_name=item.product_name).update(
                        product_shipped_number=product_shipped_number)
                    product_queryset = product_models.Product.objects.filter(product_name=item.product_name).first()
                    if product_kind == 0:
                        product_number = product_queryset.product_number - item.product_number
                        product_models.Product.objects.filter(product_name=item.product_name).update(
                            product_number=product_number)
                    else:
                        product_number = product_queryset.product_semi_finished_number - item.product_number
                        product_models.Product.objects.filter(product_name=item.product_name).update(
                            product_semi_finished_number=product_number)
            else:
                product_models.ProductShipmentNormal.objects.filter(product_shipment_id=product_shipment_id).update(
                    warehousing_confirm=-1, warehousing_confirm_time=get_time(request))
        res = {
            'code': 1,
            'msg': "处理产品出货成功"
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'msg': "处理会话失败"
        }
        return JsonResponse(res)


# 获取所有可用指令单号
def get_all_production_order_id(request):
    production_order_id_list = list(order_models.ProductionOrder.objects.values_list('production_order_id', flat=True))
    select_list = []
    for item in production_order_id_list:
        production_order_list = order_models.ProductionOrder.objects.filter(production_order_id=item).first()
        if production_order_list.quality_confirm != 1 and production_order_list.factory_manager_confirm != 1:
            continue
        temp_obj = {
            'value': item,
            'label': item
        }
        select_list.append(temp_obj)
    res = {
        'code': 1,
        'data': select_list,
        'msg': '获取指令单号列表成功'
    }
    return JsonResponse(res)


# 根据指令单号获取材料信息
def get_material_info_from_production_order_id(request):
    body = json.loads(request.body)
    production_order_id = body.get('production_order_id')
    production_order_material_list_all = order_models.LinkProductionOrderByMaterial.objects.filter(
        production_order_id=production_order_id)
    material_list = []
    list_id = 0
    for production_order_material_list in production_order_material_list_all:
        list_id = list_id + 1
        material_id = production_order_material_list.material_id
        row_data = warehouse_models.RawMaterial.objects.filter(material_id=material_id).first()
        material_name = (row_data.material_name + ' ' + row_data.material_type + ' ' + row_data.material_color + ' ' +
                         row_data.material_product_supplier + ' ' + row_data.material_supplier + ' ' + row_data.remark)
        material_kind = production_order_material_list.material_order_kind
        if material_kind == 0:
            material_kind = '原料'
        else:
            material_kind = '水口料'
        material_order_weight = production_order_material_list.material_order_weight
        material_used_weight = production_order_material_list.material_used_weight
        material_can_get = material_order_weight - material_used_weight
        temp_obj = {
            'id': list_id,
            'material_id': material_id,
            'material_name': material_name,
            'material_kind': material_kind,
            'material_order_weight': material_order_weight,
            'material_used_weight': material_used_weight,
            'material_can_get': material_can_get
        },
        material_list.append(temp_obj[0])

    res = {
        'code': 1,
        'data': material_list,
        'msg': '获取指令单对应材料列表成功'
    }
    return JsonResponse(res)


# 根据指令单号获取产品信息
def get_product_info_from_production_order_id(request):
    body = json.loads(request.body)
    production_order_id = body.get('production_order_id')
    production_order_product_list_all = order_models.LinkProductionOrderByProduct.objects.filter(
        production_order_id=production_order_id)
    product_list = []
    list_id = 0
    for production_order_product_list in production_order_product_list_all:
        list_id = list_id + 1
        product_name = production_order_product_list.product_name

        product_kind = production_order_product_list.if_semi_finished
        if product_kind == 0:
            product_kind = '成品'
        else:
            product_kind = '半成品'
        product_received_number = production_order_product_list.product_received_number
        product_shipped_number = production_order_product_list.product_shipped_number
        product_number = production_order_product_list.product_number
        product_can_storage = product_number - product_shipped_number - product_received_number
        temp_obj = {
            'id': list_id,
            'product_name': product_name,
            'product_kind': product_kind,
            'product_received_number': product_received_number,
            'product_shipped_number': product_shipped_number,
            'product_number': product_number,
            'product_can_ship': product_number - product_shipped_number,
            'product_can_storage': product_can_storage
        },
        product_list.append(temp_obj[0])

    res = {
        'code': 1,
        'data': product_list,
        'msg': '获取指令单对应产品列表成功'
    }
    return JsonResponse(res)


# 获取待审批列表
def get_approval_list(request):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    list_all = []
    if body.get('approval_number') != 0:
        if user_id == 4:
            list_all = four_approval_list(request)
        if user_id == 6:
            list_all = six_approval_list(request)
        if user_id == 2:
            list_all = two_approval_list(request)
        if user_id == 7:
            list_all = seven_approval_list(request)
        if user_id == 1:
            liat_all = one_approval_list(request)
        res = {
            'code': 1,
            'data': list_all,
            'msg': '获取审批列表成功'
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 1,
            'data': [],
            'msg': '获取审批列表成功'
        }
        return JsonResponse(res)


# 获取审批的循环
def approval_list_cycle(queryset, form_name):
    approval_list = []
    for item in queryset:
        user_queryset = login_models.User.objects.filter(user_id=item[1]).first()
        temp_obj = {
            'create_time': item[0],
            'apply_user_id': item[1],
            'true_name': user_queryset.true_name,
            'id': item[2],
            'form_name': form_name
        }
        approval_list.append(temp_obj)
    return approval_list


# 获取审批数量
def get_approval_number(request):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    number = 0
    if user_id == 4:
        number = four_approval_number(request)
    if user_id == 6:
        number = six_approval_number(request)
    if user_id == 2:
        number = two_approval_number(request)
    if user_id == 7:
        number = seven_approval_number(request)
    if user_id == 1:
        number = one_approval_number(request)
    res = {
        'code': 1,
        'data': number,
        'msg': '获取审批数量成功'
    }
    return JsonResponse(res)


# 获取列表中0的个数
def get_zero_number(list_name):
    number = 0
    for item in list_name:
        if item == 0:
            number = number + 1
    return number


# 品管审批
def four_approval_number(request):
    production_order_list_number = get_zero_number(
        list(order_models.ProductionOrder.objects.values_list('quality_confirm', flat=True)))
    production_storage_normal_list_number = get_zero_number(
        list(product_models.ProductStorageNormal.objects.values_list('quality_confirm', flat=True)))
    material_purchase_list_number = get_zero_number(
        list(warehouse_models.MaterialPurchase.objects.values_list('quality_confirm', flat=True)))
    product_shipment_list_number = get_zero_number(
        list(product_models.ProductShipmentNormal.objects.values_list('quality_confirm', flat=True)))
    return production_order_list_number + production_storage_normal_list_number + material_purchase_list_number + product_shipment_list_number


def four_approval_list(request):
    approval_list = approval_list_cycle(
        product_models.ProductStorageNormal.objects.filter(quality_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'product_storage_id'), '产品入库申请') + approval_list_cycle(
        warehouse_models.MaterialPurchase.objects.filter(quality_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_purchase_id'), '材料入库申请') + approval_list_cycle(
        order_models.ProductionOrder.objects.filter(quality_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'production_order_id'), '生产指令单申请') + approval_list_cycle(
        product_models.ProductShipmentNormal.objects.filter(quality_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'product_shipment_id'), '产品出货申请')
    return approval_list


# 仓库审批
def six_approval_number(request):
    product_shipment_list_number = get_zero_number(
        list(product_models.ProductShipmentNormal.objects.values_list('warehousing_confirm', flat=True)))
    production_storage_normal_list_number = get_zero_number(
        list(product_models.ProductStorageNormal.objects.values_list('warehousing_confirm', flat=True)))
    material_purchase_list_number = get_zero_number(
        list(warehouse_models.MaterialPurchase.objects.values_list('warehousing_confirm', flat=True)))
    material_back_number = get_zero_number(
        list(warehouse_models.MaterialBack.objects.values_list('warehousing_confirm', flat=True)))
    material_get_number = get_zero_number(
        list(warehouse_models.MaterialGetNormal.objects.values_list('warehousing_confirm', flat=True)))
    material_out_factory_number = get_zero_number(
        list(warehouse_models.MaterialOutFactory.objects.values_list('warehousing_confirm', flat=True)))
    return (product_shipment_list_number + production_storage_normal_list_number + material_purchase_list_number +
            material_back_number + material_get_number + material_out_factory_number)


def six_approval_list(request):
    approval_list = approval_list_cycle(
        product_models.ProductShipmentNormal.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'product_shipment_id'), '产品出货申请') + approval_list_cycle(
        product_models.ProductStorageNormal.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'product_storage_id'), '产品入库申请') + approval_list_cycle(
        warehouse_models.MaterialPurchase.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_purchase_id'), '材料入库申请') + approval_list_cycle(
        warehouse_models.MaterialBack.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_back_id'), '材料退库申请') + approval_list_cycle(
        warehouse_models.MaterialGetNormal.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_get_id'), '材料领取申请') + approval_list_cycle(
        warehouse_models.MaterialOutFactory.objects.filter(warehousing_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_out_factory_id'), '材料出厂申请')

    return approval_list


# 副总审批数
def two_approval_number(request):
    material_out_factory_number = get_zero_number(
        list(warehouse_models.MaterialOutFactory.objects.values_list('deputy_general_manager_confirm', flat=True)))
    return material_out_factory_number


def two_approval_list(request):
    approval_list = (
        warehouse_models.MaterialOutFactory.objects.filter(deputy_general_manager_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_out_factory_id'), '材料出厂申请')

    return approval_list


# 厂长审批
def seven_approval_number(request):
    production_order_number = get_zero_number(
        list(order_models.ProductionOrder.objects.values_list('factory_manager_confirm', flat=True)))
    material_back_number = get_zero_number(
        list(warehouse_models.MaterialBack.objects.values_list('factory_manager_confirm', flat=True)))
    material_get_number = get_zero_number(
        list(warehouse_models.MaterialGetNormal.objects.values_list('factory_manager_confirm', flat=True)))

    return material_back_number + material_get_number + production_order_number


def seven_approval_list(request):
    approval_list = approval_list_cycle(
        warehouse_models.MaterialBack.objects.filter(factory_manager_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_back_id'), '材料退库申请') + approval_list_cycle(
        warehouse_models.MaterialGetNormal.objects.filter(factory_manager_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_get_id'), '材料领取申请') + approval_list_cycle(
        order_models.ProductionOrder.objects.filter(factory_manager_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'production_order_id'), '生产指令单申请')

    return approval_list


# 总经理审批数
def one_approval_number(request):
    material_out_factory_number = get_zero_number(
        list(warehouse_models.MaterialOutFactory.objects.values_list('general_manager_confirm', flat=True)))
    return material_out_factory_number


def one_approval_list(request):
    approval_list = approval_list_cycle(
        warehouse_models.MaterialOutFactory.objects.filter(general_manager_confirm=0).values_list(
            'create_time',
            'apply_user_id', 'material_out_factory_id'), '材料出厂申请')

    return approval_list
