# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/22 20:11'

from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<code>\w+)$', active, name='active'),
    url(r'^log_out/$', log_out, name='log_out'),
    url(r'^check_user/$', check_user, name='check_user')
]