from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import EmailProfile, UserProfile
from utils.email_utils import send_email
from django.contrib.auth.hashers import make_password
from datetime import datetime
import time
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
# Create your views here.


# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'df_user/login.html')

    def post(self, request):
        """

        :param request: 0>登录失败 1>登录成功
        :return:
        """
        next_href = request.GET.get('next', '')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                result = {'status': 1, 'msg': '恭喜您!登录成功!', 'next': next_href}
                return JsonResponse(result)
            else:
                result = {'status': 0, 'msg': '登录失败!用户名或密码不正确!请检查后重试!', 'next': next_href}
                return JsonResponse(result)
        else:
            form.errors['type'] = 0
            return JsonResponse(form.errors)


# 自定义验证
class CustomVerify(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


# 注册
class RegisterView(View):
    def get(self, request):
        forms = RegisterForm()
        return render(request, 'df_user/register.html', {'forms': forms})

    def post(self, request):
        """

        :param request: 1>注册成功 2>用户名已存在 3>邮箱已被注册 4>邮件发送失败(未知错误) 5>密码不一致
        :return:
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']
            # if UserProfile.objects.filter(username=username):
            #     result = {'status': 2, 'msg': '该用户名已存在,请重新选择!'}
            #     return JsonResponse(result)
            # elif UserProfile.objects.filter(email=email):
            #     result = {'status': 3, 'msg': '该邮箱已被注册,请重新注册!'}
            #     return JsonResponse(result)
            if password != repassword:
                result = {'status': 5, 'msg': '两次密码输入不一致,请检查后重新输入!'}
                return JsonResponse(result)
            user = UserProfile()
            user.email = email
            user.password = make_password(password)
            user.is_active = 0
            user.is_staff = 0
            user.username = username
            if send_email(to_email=email, send_type='register'):
                result = {'status': 1, 'msg': '天天生鲜! 恭喜您注册成功, 激活邮件已发送至您的邮箱, 请注意查收!'}
                user.save()
                return JsonResponse(result)
            else:
                result = {'status': 4, 'msg': '天天生鲜! 恭喜您注册成功, 激活邮件发送失败, 请检查后重试或者联系客服(QQ:837497936)!'}
                return JsonResponse(result)
        else:
            form.errors['type'] = 0
            return JsonResponse(form.errors)


# 检测用户是否使用
def check_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        if UserProfile.objects.filter(username=username):
            result = {'status': 2, 'msg': '该用户名已存在,请重新选择!'}
            return JsonResponse(result)
        elif UserProfile.objects.filter(email=email):
            result = {'status': 3, 'msg': '该邮箱已被注册,请重新输入!'}
            return JsonResponse(result)


# 激活账户
def active(request, code):
    emailRecord = EmailProfile.objects.filter(code=code)
    if emailRecord:
        emailRecord = emailRecord[0]
        if emailRecord.status:
            return HttpResponse('该验证连接已失效! 请重新注册!')
        now = datetime.now()
        now_time = time.mktime(now.timetuple())
        exprie_time = time.mktime(emailRecord.exprie_time.timetuple())
        if now_time > exprie_time:
            return HttpResponse('激活邮件失败')
        user = UserProfile.objects.get(email=emailRecord.email)
        user.is_active = 1
        user.is_staff = 0
        user.save()
        emailRecord.status = True
        emailRecord.save()
        return HttpResponse('<a href="http://127.0.0.1:8000/user/login/">您的账号{}已激活成功, 点击登录</a>'.format(user.email))
    else:
        return HttpResponse('您访问的激活链接不存在, 请检查后重新访问!')


# 找回密码
class ForgetView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


# 注销
def log_out(request):
    logout(request)
    return redirect('/')
