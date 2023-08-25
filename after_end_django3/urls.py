"""after_end_django3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views as login_views
from warehouse import views as warehouse_views
from order import views as order_views
from product import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_views.login),
    path('getDeviceInfo', login_views.get_computer_info),
    path('changeUserInfo', login_views.change_user_info),
    path('imgUpload', login_views.img_upload),
    path('getMaterialStock', warehouse_views.get_material_stock),
    path('materialPurchase', warehouse_views.material_purchase),
    path('getAllMaterialName', warehouse_views.get_all_material_name),
    path('materialBack', warehouse_views.material_back),
    path('makeProductionOrder', order_views.make_production_order),
    path('getAllProductName', product_views.get_all_product_name),
    path('addNewProduct', product_views.add_new_product),
    path('addNewMaterial', warehouse_views.add_new_material),
    path('materialOutFactory', warehouse_views.material_out_factory),
    path('materialGetNormal', warehouse_views.material_get_normal),
    path('getAllProductionOrderId', order_views.get_all_production_order_id),
    path('getMaterialInfoByProductionOrderId', order_views.get_material_info_from_production_order_id),
    path('productStorageNormal', product_views.product_storage_normal),
    path('getProductInfoByProductionOrderId', order_views.get_product_info_from_production_order_id),
    path('productShipment', product_views.product_shipment),
    path('getApprovalNumber', order_views.get_approval_number),
    path('getApprovalList', order_views.get_approval_list),
    path('getApprovalDialogData', order_views.get_approval_dialog_data),
    path('handelApprovalResult', order_views.handel_approval_result),
    path('getProductStock',product_views.get_product_stock),
    path('getMaterialNameById',warehouse_views.get_material_name_by_id),
    path('getAllMaterialOrderTestId',order_views.get_all_material_test_order_id),
    path('makeMaterialTestOrder',order_views.make_material_test_order)
]
