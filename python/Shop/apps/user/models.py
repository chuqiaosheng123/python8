from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from datetime import datetime
# Create your models here.


#  用户
class UserProfile(AbstractUser):
    # 收件人
    income_name = models.CharField(max_length=50, verbose_name='收件人', null=True)
    address = models.CharField(max_length=100, verbose_name='用户地址')
    phone = models.CharField(max_length=11, null=False, verbose_name='手机号')
    image = models.ImageField(upload_to='images/head/%Y/%m/', verbose_name='用户头像')
    postcode = models.CharField(max_length=50, null=True, verbose_name='邮编')

    class Meta:
        db_table = 'df_user_userprofile'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 邮箱
class EmailProfile(models.Model):
    # 验证码
    code = models.CharField(max_length=50, null=False, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='用户邮箱')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')
    exprie_time = models.DateTimeField(null=True, verbose_name='过期时间')
    send_type = models.CharField(choices=(('register', '注册邮件'), ('forget', '找回密码')), max_length=10, verbose_name='邮件类型')
    status = models.BooleanField(choices=((True, '已使用'), (False, '未使用')), verbose_name='邮件状态', default=False)

    class Meta:
        verbose_name = '邮箱'
        verbose_name_plural = verbose_name
