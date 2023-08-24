import json

from django.http import JsonResponse
from warehouse import models as warehouse_models
from login import models as login_models
from product import models as product_models
from order import models as order_models


# Create your views here.
# 获取产品库存
def get_product_stock(request):
    data_array = []
    for item in product_models.Product.objects.all():
        stock_obj = {
            'product_id': item.product_id,
            'product_name': item.product_name,
            'product_number': item.product_number,
            'product_semi_finished_number': item.product_semi_finished_number,
            'shelf_number': item.shelf_number,

        }
        data_array.append(stock_obj)
    res = {
        'code': 1,
        'data': data_array,
        'msg': "获取产品库存成功"
    }
    return JsonResponse(res)


# 向产品表中新增产品
def add_new_product(request):
    body = json.loads(request.body)
    if product_models.Product.objects.filter(product_name=body.get('new_product_name')):
        res = {
            'code': 0,
            'msg': '该产品已存在，请勿重复添加'
        }
        return JsonResponse(res)
    else:
        product_models.Product.objects.create(product_name=body.get('new_product_name'))
        res = {
            'code': 1,
            'msg': '新增产品成功'
        }
        return JsonResponse(res)


# 获取所有产品名
def get_all_product_name(request):
    product_name_list = list(product_models.Product.objects.values_list('product_name', flat=True))
    select_list = []
    for item in product_name_list:
        temp_obj = {
            'value': item,
            'label': item
        }
        select_list.append(temp_obj)
    res = {
        'code': 1,
        'data': select_list,
        'msg': '获取产品列表成功'
    }
    return JsonResponse(res)


# 产品入库
def product_storage_normal(request):
    body = json.loads(request.body)
    # 判断指令单是否存在以及指令单状态
    if order_models.ProductionOrder.objects.filter(
            production_order_id=body.get('production_order_id')) and order_models.ProductionOrder.objects.filter(
        production_order_status=1):

        # 写入材料入库基本表
        product_models.ProductStorageNormal.objects.create(apply_user_id=body.get('user_id'),
                                                           create_time=body.get('create_time'),
                                                           production_order_id=body.get('production_order_id'),
                                                           product_storage_img=body.get('product_storage_img'))

        # 获取新增的基本表数据的id以及需要领取的材料列表
        product_storage_list = product_models.ProductStorageNormal.objects.filter(
            create_time=body.get('create_time')).first()
        product_storage_id = product_storage_list.product_storage_id
        product_list = body.get('product_list')

        # 循环便利需要入库的列表
        for item in product_list:

            # 判断该产品是否存在
            if product_models.Product.objects.filter(product_name=item.get('product_name')):
                # 判断是否超出该订单对应原料可领取数量
                production_order_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                    production_order_id=body.get('production_order_id'), product_name=item.get('product_name')).first()
                # 判断需要入库的产品是否就是指令单的产品
                if production_order_queryset.product_name == item.get('product_name'):
                    can_storage_number = (production_order_queryset.product_number -
                                          production_order_queryset.product_received_number)
                    if can_storage_number > 0 and item.get('product_number') <= can_storage_number:
                        product_models.LinkProductStorageNormal.objects.create(product_storage_id=product_storage_id,
                                                                               product_name=item.get('product_name'),
                                                                               product_number=item.get(
                                                                                   'product_number')),

                    else:
                        product_models.ProductStorageNormal.objects.filter(
                            product_storage_id=product_storage_id).delete()
                        res = {
                            'code': 0,
                            'data': '',
                            'msg': '订单已满，多余部分无法入库'
                        }
                        return JsonResponse(res)
                else:
                    product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).delete()
                    res = {
                        'code': 0,
                        'data': '',
                        'msg': '非指令单产品，无法入库'
                    }
                    return JsonResponse(res)

            else:
                # 删除基本表刚写入数据
                product_models.ProductStorageNormal.objects.filter(product_storage_id=product_storage_id).delete()
                res = {
                    'code': 0,
                    'data': '',
                    'msg': '产品不存在'
                }
                return JsonResponse(res)
        res = {
            'code': 1,
            'data': '',
            'msg': '产品入库成功'
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'data': '',
            'msg': '指令单不存在或指令单未激活'
        }
        return JsonResponse(res)


# 产品出货
def product_shipment(request):
    body = json.loads(request.body)
    # 判断指令单是否存在以及指令单状态
    if order_models.ProductionOrder.objects.filter(
            production_order_id=body.get('production_order_id')) and order_models.ProductionOrder.objects.filter(
        production_order_status=1):

        # 写入材料入库基本表
        product_models.ProductShipmentNormal.objects.create(apply_user_id=body.get('user_id'),
                                                            create_time=body.get('create_time'),
                                                            production_order_id=body.get('production_order_id'),
                                                            product_shipment_img=body.get('product_shipment_img'))

        # 获取新增的基本表数据的id以及需要领取的材料列表
        product_shipment_list = product_models.ProductShipmentNormal.objects.filter(
            create_time=body.get('create_time')).first()
        product_shipment_id = product_shipment_list.product_shipment_id
        product_list = body.get('product_list')

        # 循环便利需要入库的列表
        for item in product_list:

            # 判断该产品是否存在
            if product_models.Product.objects.filter(product_name=item.get('product_name')):
                # 判断是否超出该订单
                production_order_queryset = order_models.LinkProductionOrderByProduct.objects.filter(
                    production_order_id=body.get('production_order_id'), product_name=item.get('product_name')).first()
                # 判断需要入库的产品是否就是指令单的产品
                if production_order_queryset.product_name == item.get('product_name'):
                    can_ship_number = (production_order_queryset.product_number -
                                       production_order_queryset.product_shipped_number)
                    product_number_stock_queryset = product_models.Product.objects.filter(
                        product_name=item.get('product_name')).first()
                    if production_order_queryset.if_semi_finished == 0:
                        product_number_stock = product_number_stock_queryset.product_number
                    else:
                        product_number_stock = product_number_stock_queryset.product_semi_finished_number
                    # 可出货量与实际库存比较
                    if 0 < item.get('product_number') < product_number_stock:
                        product_models.LinkProductShipmentNormal.objects.create(product_shipment_id=product_shipment_id,
                                                                                product_name=item.get('product_name'),
                                                                                product_number=item.get(
                                                                                    'product_number')),

                    else:
                        product_models.ProductShipmentNormal.objects.filter(
                            product_shipment_id=product_shipment_id).delete()
                        res = {
                            'code': 0,
                            'data': '',
                            'msg': '订单已出货完毕，或库存不足'
                        }
                        return JsonResponse(res)
                else:
                    product_models.ProductShipmentNormal.objects.filter(
                        product_shipment_id=product_shipment_id).delete()
                    res = {
                        'code': 0,
                        'data': '',
                        'msg': '非指令单产品，无法出货'
                    }
                    return JsonResponse(res)

            else:
                # 删除基本表刚写入数据
                product_models.ProductShipmentNormal.objects.filter(product_shipment_id=product_shipment_id).delete()
                res = {
                    'code': 0,
                    'data': '',
                    'msg': '产品不存在'
                }
                return JsonResponse(res)
        res = {
            'code': 1,
            'data': '',
            'msg': '产品出货成功'
        }
        return JsonResponse(res)
    else:
        res = {
            'code': 0,
            'data': '',
            'msg': '指令单不存在或指令单未激活'
        }
        return JsonResponse(res)
