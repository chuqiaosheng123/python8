# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/26 11:24'

from django import template
register = template.Library()

@register.filter
def key(d, key):
    return d[key]