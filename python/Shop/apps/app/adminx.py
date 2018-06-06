# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/23 19:51'
import xadmin
from .models import  *


class OrderAdmin(object):
    list_display = ['user', 'o_date', 'o_pay', 'o_total_price']


xadmin.site.register(Order, OrderAdmin)


class TypeAdmin(object):
    list_display = ['title', 'class_name', 'type_img']


xadmin.site.register(Commodity_type, TypeAdmin)


class CommodityAdmin(object):
    list_display = ['g_title', 'g_pic', 'g_price', 'g_unit', 'g_click', 'g_desc', 'g_stock', 'content', 'g_type']
    style_fields = {'content': 'ueditor'}


xadmin.site.register(Commodity, CommodityAdmin)


class DetailinfoAdmin(object):
    list_display = ['count', 'order', 'goods']


xadmin.site.register(Detailinfo, DetailinfoAdmin)


class ShoopCartAdmin(object):
    list_diaplay = ['count', 'user', 'good']


xadmin.site.register(ShoopCart, ShoopCartAdmin)