from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .messages import Message,Signature,Access_Token,Menu

@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 取出认证参数

        result = Signature.check_signature(request)

        if result:
            Menu.create_menu()

        #返回验证结果


        return HttpResponse(result)

    elif request.method == 'POST':

        msg = Message(request.body)
        result = msg.process_from_msgtype()

        return HttpResponse(result,content_type='xml/application')




















