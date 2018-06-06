# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/22 22:42'
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=6, max_length=20, required=True)
    repassword = forms.CharField(min_length=6, max_length=20, required=True)
    email = forms.EmailField(required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(min_length=6, max_length=20, required=True)


class ForgetForm(forms.Form):
    pass
