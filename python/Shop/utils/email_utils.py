# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/23 9:17'
import random
from django.core.mail import send_mail
from user.models import EmailProfile
from datetime import datetime
import datetime
from Shop import settings


# 验证码
def security_code():
    string = 'qwertyuiopLKJHGFDSAzxcvBNM123456789'
    code = ''
    for x in range(16):
        code += random.choice(string)
    return code


# 邮件发送
def send_email(to_email, send_type='register'):
    email = EmailProfile()
    email.code = security_code()
    email.email = to_email
    email.send_type = send_type
    # 邮件过期时间 = 现在的时间+7天
    email.exprie_time = datetime.datetime.now() + datetime.timedelta(days=7)
    try:
        title = ''
        content = ''
        if send_type == 'register':
            title = '天天生鲜!账号激活邮件!'
            content = '欢迎注册天天生鲜,点击链接激活您的账户<a href="http://39.107.250.165:8000/user/active/{}">http://39.107.250.165:8000/user/active/{}</a>'.format(email.code, email.code)
        else:
            title = '天天生鲜!密码找回邮件!'
            content = '该邮件为天天生鲜密码找回邮件!如不是本人操作,请忽视该邮件.点击链接找回您的密码'
        res = send_mail(title, '', settings.EMAIL_HOST_USER, [to_email], html_message=content)
        if res == 1:
            # 保存
            email.save()
            return True
        else:
            return False
    except Exception as e:
        return False


