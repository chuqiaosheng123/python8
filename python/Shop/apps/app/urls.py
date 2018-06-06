# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/22 20:09'


from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^center/$', usercenter, name='center'),
    url(r'^orders/$', orders, name='orders'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^fruits/$', fruits, name='fruits'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^add_cart/$', add_cart, name='add_cart'),
    url(r'^update_cart/$', update_cart, name='update_cart'),
    url(r'^delete_cart/$', delete_cart, name='delete_cart'),
    url(r'^add_order/$', add_order, name='add_order'),
    url(r'^check_pay/$', check_pay, name='check_pay'),
    url(r'^address/$', address, name='address'),
    url(r'^order_goods/$', order_goods, name='order_goods'),
    url(r'^$', index, name='index'),

]