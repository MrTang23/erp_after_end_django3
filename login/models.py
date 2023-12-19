from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(verbose_name='用户id', primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=16, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    true_name = models.CharField(verbose_name='真实姓名', max_length=6)
    role_id = models.IntegerField(verbose_name='身份码')

