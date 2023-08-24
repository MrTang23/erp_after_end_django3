from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(verbose_name='用户id', primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=16, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    true_name = models.CharField(verbose_name='真实姓名', max_length=6)
    role_id = models.IntegerField(verbose_name='身份码')

#
# User.objects.create(user_id=1, username="tangaozhong", password="123456", true_name="汤敖忠", role_id=1)
# User.objects.create(user_id=2, username="zhangwei", password="123456", true_name="张伟", role_id=2)
# User.objects.create(user_id=3, username="tianjiane", password="123456", true_name="田建娥", role_id=7)
# User.objects.create(user_id=4, username="xiangyan", password="123456", true_name="向艳", role_id=6)
# User.objects.create(user_id=5, username="wanglijuan", password="123456", true_name="王礼娟", role_id=5)
# User.objects.create(user_id=6, username="yuxuwen", password="123456", true_name="余旭文", role_id=4)
# User.objects.create(user_id=7, username="ketao", password="123456", true_name="柯涛", role_id=3)
