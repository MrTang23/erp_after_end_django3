import copy

from django.http import JsonResponse

from warehouse import models as warehouse_models
from product import models as product_models


# Create your views here.
def get_material_purchase_list(request):
    # 假设已经从数据库查询到了查询集
    material_purchases = warehouse_models.MaterialPurchase.objects.all().values()
    main_list = []
    # 遍历查询集，获取每个对象的内容
    for purchase in material_purchases:
        material_list = warehouse_models.LinkMaterialPurchase.objects.filter(
            material_purchase_id=purchase['material_purchase_id']).values()
        for items in material_list:
            raw_material = warehouse_models.RawMaterial.objects.filter(material_id=items['material_id']).values()
            items = {**items, **raw_material[0]}
            main_list.append({**items, **purchase})
    res = {
        'code': 1,
        'data': main_list,
        'msg': '获取成功'
    }
    return JsonResponse(res)


def find_purchase_list(purchase_id, purchase):
    material_list = warehouse_models.LinkMaterialPurchase.objects.filter(material_purchase_id=purchase_id).values()
    detail_list = []
    for items in material_list:
        raw_material = warehouse_models.RawMaterial.objects.filter(material_id=items['material_id']).values()
        items = {**items, **raw_material[0]}
        detail_list.append({**items, **purchase})
    return detail_list


def get_material_get_list(request):
    material_purchases = warehouse_models.MaterialGetNormal.objects.all().values()
    main_list = []
    # 遍历查询集，获取每个对象的内容
    for item in material_purchases:
        material_list = warehouse_models.LinkMaterialGetNormal.objects.filter(
            material_get_id=item['material_get_id']).values()
        for items in material_list:
            raw_material = warehouse_models.RawMaterial.objects.filter(material_id=items['material_id']).values()
            merged_items = {**raw_material[0], **items, **item}
            main_list.append(merged_items)
    res = {
        'code': 1,
        'data': main_list,
        'msg': '获取成功'
    }
    return JsonResponse(res)


def get_product_storage_list(requests):
    product_storage = product_models.ProductStorageNormal.objects.all().values()
    main_list = []
    # 遍历查询集，获取每个对象的内容
    for item in product_storage:
        product_list = product_models.LinkProductStorageNormal.objects.filter(
            product_storage_id=item['product_storage_id']).values()
        for items in product_list:
            merged_items = {**items, **item}
            main_list.append(merged_items)
    res = {
        'code': 1,
        'data': main_list,
        'msg': '获取成功'
    }
    return JsonResponse(res)


def get_product_shipment_list(requests):
    product_shipment = product_models.ProductShipmentNormal.objects.all().values()
    main_list = []
    for item in product_shipment:
        product_list = product_models.LinkProductShipmentNormal.objects.filter(
            product_shipment_id=item['product_shipment_id']
        ).values()
        for items in product_list:
            merged_items = {**items, **item}
            main_list.append(merged_items)
    res = {
        'code': 1,
        'data': main_list,
        'msg': '获取成功'
    }
    return JsonResponse(res)