# -*- coding: utf-8 -*-
# __author__ = 'ZKL'
# __date__ = '2018/5/23 19:51'
from .models import UserProfile, EmailProfile
from xadmin.views import CommAdminView, BaseAdminView
import xadmin


class CustomView(object):
    site_title = '天天生鲜后台管理'
    site_footer = '自定义版权信息'
    menu_style = 'accordion'


xadmin.site.register(CommAdminView, CustomView)


class ThemeView(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(BaseAdminView, ThemeView)


class EmailAdmin(object):
    # 展示字段
    list_display = ['code', 'email', 'send_type', 'send_time', 'status']
    # 搜索字段
    search_fields = ['email', 'send_type']
    # 筛选器字段
    list_filter = ['send_time']
    # 只读字段,后台管理中只能读取不能修改
    readonly_fields = ['code', 'email']
    # 在列表页允许修改的页面
    list_editable = ['send_type', 'status']
    # 自动刷新
    refresh_times = [3,5]
    # 按照某字段排序
    # ordering = ['-send_time']
    # 配置插件效果


xadmin.site.register(EmailProfile, EmailAdmin)