import json
import os
import time

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from login.models import User
from django.shortcuts import render


# Create your views here.
# 获取客户端设备信息 get
def get_computer_info(request):
    res = {
        "ip": request.META['REMOTE_ADDR'],
        "host": request.META['REMOTE_HOST'],
        "user_agent": request.headers.get("user-agent")
    }
    return JsonResponse(res)


# 登陆 post
def login(request):
    body = json.loads(request.body)
    username = body.get('username')
    password = body.get('password')
    if User.objects.filter(username=username):
        user_info = User.objects.filter(username=username).first()
        if user_info.password == password:
            res = {
                "code": 1,
                'data': {
                    'username': username,
                    'password': password,
                    'role_id': user_info.role_id,
                    'true_name': user_info.true_name,
                    'user_id': user_info.user_id
                },
                'msg': '登陆成功'
            }
        else:
            res = {
                "code": 0,
                "msg": "密码错误"
            }
    else:
        res = {
            "code": 0,
            "msg": "用户不存在"
        }
    return JsonResponse(res)


# 更改密码 post
def change_user_info(request):
    body = json.loads(request.body)
    user_id = body.get('user_id')
    new_password = body.get('new_password')
    new_username = body.get('new_username')
    if User.objects.filter(user_id=user_id):
        User.objects.filter(user_id=user_id).update(password=new_password)
        User.objects.filter(user_id=user_id).update(username=new_username)
        res = {
            "code": 1,
            "msg": "个人信息更新成功"
        }
    else:
        res = {
            "code": 0,
            "msg": "更新失败"
        }
    return JsonResponse(res)


# 图片上传接口
def img_upload(request):
    file = request.FILES['file']
    root = '%s/%s' % (settings.IMAGE, file)
    with open(root, 'wb') as f:
        for i in file.chunks():
            f.write(i)
    file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.jpeg'
    os.rename(root, settings.IMAGE + '/' + file_name)
    res = {
        'code': 1,
        'data': {
            'file_path': settings.IMAGE + '/' + file_name,
            'file_name': file_name
        },
        'msg': '图片上传成功'
    }
    return JsonResponse(res)


# 获取图片接口
def get_image(request):
    url = request.GET.get('url')
    path = repr(settings.IMAGE + '/' + url)
    path = eval(path)
    path = str(path)
    file_one = open(path, "rb")
    return HttpResponse(file_one.read(), content_type='image/jpg')
