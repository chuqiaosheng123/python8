# -*- coding: utf-8 -*-
__author__ = 'chu'
__date__ = '2018/6/4 9:39'

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from xml.etree import ElementTree
import time
import datetime
from xml import etree
from WeChat import settings
import requests
import json
# 处理消息的类
'''
<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[{}]]></MediaId></Image></xml>
'''

# 回复文本消息的格式
TEXT_TEMPLATE = """<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[{}]]></Content></xml>"""

IMAGE_TEMPLATE = '''<xml><ToUserName><![CDATA[{}]]></ToUserName><FromUserName><![CDATA[{}]]></FromUserName><CreateTime>{}</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[{}]]></MediaId></Image></xml>'''


class Message(object):
    def __init__(self, body):
        """

        :param body: 微信服务器端发过来的数据,xml
        """
        self.body = body
        self.MsgType = ''
        self.FromUserName = ''
        self.ToUserName = ''
        self.CreateTime = ''
        self.MediaId = ''
        self.MsgId = ''
        self.Event = ''
        self.Content = ''  # 接收的文本信息
        self.xmlTransAttr()

    def xmlTransAttr(self):

        eleTree = ElementTree.fromstring(self.body)
        if eleTree.tag == 'xml':
            for child in eleTree:
                setattr(self, child.tag, child.text)

    # 处理各种消息的函数
    def process_from_msgtype(self):

        result = ''
        # 判断消息类型
        if self.MsgType == 'text':
            result = self.textMsg()

        elif self.MsgType == 'image':
            pass

        elif self.MsgType == 'voice':
            pass

        elif self.MsgType == 'video':
            pass

        elif self.MsgType == 'event':

            if self.Event == 'subscribe':
                pass

            elif self.Event == 'unsubscribe':
                pass

            elif self.Event == 'CLICK':
                pass

            elif self.Event == 'VIEW':
                pass

        # 返回最终的结果
        return result

    # 处理文本的事件
    def textMsg(self):
        # 取出文本消息内容
        if self.Content:
            url = 'http://api.map.baidu.com/telematics/v3/weather?location={}&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'.format(
                self.Content)
            # 发送请求 拿回数据
            rs_dict = requests.get(url).json()
            # 判断城市名称是否正确
            if rs_dict['error'] != 0:
                # 不正确,返回错误信息
                return TEXT_TEMPLATE.format(self.FromUserName, self.ToUserName, time.time(), '您输入的城市不存在,请检查后重试')

            else:
                # 查询的城市
                wea_dict = rs_dict['results'][0]
                city = wea_dict['currentCity']
                pm25 = float(wea_dict['pm25'])
                pollute = ''
                # 判断pm值得范围
                if 35 >= pm25 > 0:
                    pollute = '[龇牙]优[龇牙]'
                elif pm25 <= 75:
                    pollute = '[白眼]良[白眼]'
                elif pm25 <= 115:
                    pollute = '[晕]轻度污染[晕]'
                elif pm25 <= 150:
                    pollute = '[难过]中度污染[难过]'
                elif pm25 <= 250:
                    pollute = '[吐]重度污染[吐]'
                else:
                    pollute = '[再见]严重污染[再见]'
                # 取出今天天气信息
                today = wea_dict['weather_data'][0]

                # 返回的文本信息
                content = '[玫瑰][玫瑰][玫瑰]{}[玫瑰][玫瑰][玫瑰]\npm值: {} \n污染指数: {}\n实时温度: {}\n天气: {}\n风级: {}\n 温度: {}'.format(
                    city, pm25, pollute, today['date'], today['weather'], today['wind'], today['temperature'])

                return TEXT_TEMPLATE.format(self.FromUserName, self.ToUserName, time.time(), content)


class Signature(object):
    TOKEN = settings.WECHAT_TOKEN

    @classmethod
    def check_signature(cls, request):
        try:
            echostr = request.GET.get('echostr')
            nonce = request.GET.get('nonce')
            signature = request.GET.get('signature')
            timestamp = request.GET.get('timestamp')

            tmplist = [cls.TOKEN, timestamp, nonce]
            tmplist.sort()

            # 将三个参数拼接成一个字符串
            tmpstr = ''.join(tmplist)
            # 对字符串进行哈希算法的加密
            hascode = hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()
            # 验证加密后的字符串和signature是否相同,相同表示该请求源自于微信
            if hascode == signature:
                return echostr

        except Exception as e:

            return None


# 获取access_token
class Access_Token(object):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
        settings.WECHAT_APPID, settings.WECHAT_SECRET)
    access_token = ''
    expires_time = ''
    expire_time = None

    @classmethod
    def get_access_token(cls):
        # 判断过期时间
        if cls.access_token and cls.expire_time >= float(time.time()):
            return cls.access_token

        else:
            cls.get_access_token_from_url()
            return cls.access_token

    @classmethod
    def set_access_token(cls, access_token):
        cls.access_token = access_token

    @classmethod
    def get_access_token_from_url(cls):
        # 发起请求拿回数据
        response = requests.get(cls.url).json()
        if response.get('access_token', None):
            cls.set_access_token(response['access_token'])
            expires_in = response['expires_in']
            cls.expire_time = float(time.time()) + float(expires_in)


# 创建自定义菜单类
class Menu(object):

    @classmethod
    def create_menu(cls):
        # 拼接url地址
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(Access_Token.get_access_token())
        data = {
            "button": [
                {
                    "name": "2",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "2-1",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "view",
                            "name": "2-2",
                            "url": "http://mp.weixin.qq.com",

                        },
                        {
                            "type": "click",
                            "name": "2-3",
                            "key": "2-3"
                        }]
                },
                {
                    "name": "3",
                    "sub_button": [
                        {
                            "type": "scancode_push",
                            "name": "3-1",
                            "key": "3-1",
                            "sub_button": []
                        },
                        {
                            "type": "scancode_push",
                            "name": "3-2",
                            "key": "3-2",
                            "sub_button": []
                        },
                        {
                            "name": "3-3",
                            "type": "location_select",
                            "key": "3-3"
                        }
                    ]
                },
                {
                    "name": "4",
                    "sub_button": [
                        {
                            "type": "pic_sysphoto",
                            "name": "4-1",
                            "key": "4-1",
                            "sub_button": []
                        },
                        {
                            "type": "pic_photo_or_album",
                            "name": "4-2",
                            "key": "4-2",
                            "sub_button": []
                        },
                        {
                            "type": "pic_weixin",
                            "name": "4-3",
                            "key": "4-3",
                            "sub_button": []
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, data=json.dumps(data))

        print(response.json())

