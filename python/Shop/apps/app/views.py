from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.views import login_required
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from alipay import AliPay
from Shop import settings
import os
# Create your views here.


# 首页
def index(request):
    infos = Commodity_type.objects.all()
    my_cart_count = ShoopCart.objects.filter(user_id=request.user.id).count()
    result = {}
    shop = {}
    # 人气商品
    hot_goods = {}
    for info in infos:
        shop[info.title] = info.commodity_set.all()[:4]
        hot_goods[info.title] = info.commodity_set.all().order_by('-g_click')[:4]
    result['shop'] = shop
    result['infos'] = infos
    result['type'] = 'goods'
    result['hot_goods'] = hot_goods
    result['my_cart_count'] = my_cart_count
    return render(request, 'df_goods/index.html', result)


# 用户中心
@login_required
def usercenter(request):
    if request.method == 'GET':
        result = {
            'type': 'user',
            'info': '1'
        }
        goods_id = request.COOKIES.get('goods_id', None)
        if goods_id:
            goods_info = [Commodity.objects.get(id=g_id) for g_id in goods_id.split(',')]
            result['goods_info'] = goods_info
        return render(request, 'df_user/user_center_info.html', result)


# 收货地址
def address(request):
    if request.method == 'GET':
        infos = UserProfile.objects.get(id=request.user.id)
        result = {}
        result['site'] = '1'
        result['type'] = 'goods'
        result['infos'] = infos
        return render(request, 'df_user/user_center_site.html', result)
    elif request.method == 'POST':
        income_name = request.POST.get('income_name')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        if income_name and address and postcode and phone:
            user = UserProfile.objects.get(id=request.user.id)
            user.income_name = income_name
            user.address = address
            user.postcode = postcode
            user.phone = phone
            user.save()
            result = {
                'status': 1,
                'msg': '提交成功!'
            }
            return JsonResponse(result)

        else:
            result = {
                'status': 0,
                'msg': '请全部填写后在提交!'
            }
            return JsonResponse(result)


# 我的订单
def order_goods(request):
    order_infos = Order.objects.filter(user_id=request.user.id)
    result = {}
    result['order'] = '1'
    result['type'] = 'cart'
    page_num = request.GET.get('page', 1)
    info = Paginator(order_infos, 3)
    try:
        infos = info.page(page_num)
    except PageNotAnInteger as e:
        infos = info.page(1)
    except Exception as e:
        if page_num > info.num_pages:
            infos = info.page(info.num_pages)
        else:
            infos = info.page(1)
    result['infos'] = infos
    return render(request, 'df_user/user_center_order.html', result)


# 我的购物车
@login_required
def cart(request):
    if request.method == 'GET':
        all_cart = ShoopCart.objects.filter(user_id=request.user.id)
        result = {
            'type': 'cart',
            'all_cart': all_cart,
        }
        return render(request, 'df_cart/cart.html', result)


# 因为这里面需要进行传参到登录界面然后在根据参数拼接url然后跳转到登录之前的页面所以只能分开写.
def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                shop_id = request.POST.get('shop_id')
                count = request.POST.get('count')
                try:
                    cart = ShoopCart.objects.get(good_id=shop_id, user_id=request.user.id, count=count)
                except Exception as e:
                    cart = ShoopCart(good_id=shop_id, count=count, user_id=request.user.id)
                else:
                    cart.count += int(count)
                cart.save()
            except Exception as e:
                print(e)
                return JsonResponse({
                    'status': 2,
                    'msg': '加入购物车失败!'
                })
            else:
                return JsonResponse({
                    'status': 1,
                    'msg': '加入购物车成功!',
                    'count': ShoopCart.objects.filter(user_id=request.user.id).count()
                })
        else:
            next_href = request.POST.get('next_href')
            next_href = next_href.split('8000')[1]
            print(next_href)
            return JsonResponse({
                'errMsg': '请先登录',
                'url': '/user/login/?next={}'.format(next_href),
                'status': 0
            })


# 修改购物车
def update_cart(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        count = request.GET.get('count')
        try:
            cart = ShoopCart.objects.get(id=c_id)
            cart.count = count
            cart.save()
        except Exception as e:
            return JsonResponse({
                'status': 0,
                'msg': '添加数量失败!'
            })
        else:
            return JsonResponse({
                'status': 1,
                'msg':'添加成功',
                'count':cart.count
            })


# 删除购物车
def delete_cart(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        try:
            cart = ShoopCart.objects.get(id=c_id)
            cart.delete()
        except Exception as e:
            return JsonResponse({
                'status': 0,
                'msg': '删除失败!'
            })
        else:
            return JsonResponse({
                'status': 1,
                'msg': '删除成功!'
            })


# 用户订单
@login_required
def orders(request):
    if request.method == 'GET':
        user = UserProfile.objects.get(id=request.user.id)
        result = {}
        result['type'] = 'user'
        result['user'] = user
        return render(request, 'df_order/place_order.html', result)
    elif request.method == 'POST':
        cart_list = [ShoopCart.objects.get(id=c_id) for c_id in request.POST.getlist('cartid')]
        result = {
            'type': 'cart',
            'cart_list': cart_list
        }
        return render(request, 'df_order/place_order.html', result)


# 创建订单
def add_order(request):
    if request.method == 'POST':
        # php和一些web框架约定[]
        cartlist = request.POST.getlist('cartlist[]')
        total_price = request.POST.get('total_price')
        # 创建订单
        order = Order()
        # 订单编号 下单时间加商品id
        order.o_id = '{}{}'.format(datetime.now().strftime('%Y%m%d%H%M%S'), request.user.id)
        order.user_id = request.user.id
        order.o_total_price = total_price
        order.save()
        for shop_id in cartlist:
            cart = ShoopCart.objects.get(id=shop_id)
            order_detail = Detailinfo()
            order_detail.goods = cart.good
            order_detail.order = order
            order_detail.count = cart.count
            order_detail.save()
            # 订单信息和订单详情保存之后,删除购物车中的商品
            cart.delete()
        ali_pay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'keys/pri'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'keys/pub'),
            debug=False
)
        order_string = ali_pay.api_alipay_trade_page_pay(
            out_trade_no=order.o_id,
            total_amount=total_price,
            subject='天天生鲜购物订单-{}'.format(order.o_id),
            return_url='https://www.baidu.com'
        )
        url = settings.ALIPAY_URL + '?' + order_string
        return JsonResponse({
            'status': 1,
            'msg': '支付成功',
            'url': url,
            'o_id': order.o_id
        })


# 检测订单是否支付
def check_pay(request):
    if request.method == 'GET':
        o_id = request.GET.get('o_id')
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(settings.BASE_DIR, 'keys/pri'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'keys/pub'),
            sign_type='RSA2',
            debug=True
        )
        while True:
            response = alipay.api_alipay_trade_query(o_id)
            code = request.get('code')
            trade_status = response.get('trade_status')
            if code == '10000' and trade_status == 'TRADE_SUCCESS':
                return JsonResponse({
                    'status': 1,
                    'msg': '支付成功'
                })
            elif(code == '10000' and trade_status == 'WAIT_BUYER_PAY') or code == '40004':
                continue
            else:
                return JsonResponse({
                    'status': 0,
                    'msg': '支付失败'
                })


# 新鲜水果/查看更多
def fruits(request):
    if request.method == 'GET':
        all_info = Commodity_type.objects.all()
        # s水果分类id
        result = {}
        type_id = request.GET.get('type_id')
        # 新品推荐
        push_infos = Commodity.objects.filter(g_type_id=type_id).order_by('-id')[:2]
        # 获取排序的方式
        sort_type = request.GET.get('type', 'default')
        if sort_type == 'default':
            infos = Commodity.objects.filter(g_type_id=type_id)
        elif sort_type == 'price':
            infos = Commodity.objects.filter(g_type_id=type_id).order_by('g_price')
        elif sort_type == 'hot':
            infos = Commodity.objects.filter(g_type_id=type_id).order_by('-g_click')
        page_num = request.GET.get('page', 1)
        content = Paginator(infos, 4)
        try:
            contents = content.page(page_num)
        except PageNotAnInteger as e:
            contents = content.page(1)
        except EmptyPage as e:
            if page_num > content.num_pages:
                contents = content.page(content.num_pages)
            else:
                contents = content.page(1)
        result['sort_type'] = sort_type
        result['contents'] = contents
        result['type_id'] = type_id
        result['type'] = 'goods'
        result['push_infos'] = push_infos
        result['all_info'] = all_info
        return render(request, 'df_goods/list.html', result)


# 详情
def detail(request):
    if request.method == 'GET':
        # 商品分类
        all_info = Commodity_type.objects.all()
        fruit_id = request.GET.get('fruit_id')
        try:
            infos = Commodity.objects.get(id=fruit_id)
        except Exception as e:
            return HttpResponse('404')
        else:
            infos.g_click += 1
            infos.save()
            result = {
                'all_info': all_info,
                'infos': infos,
                'type': 'goods',
                'my_cart_count': ShoopCart.objects.filter(user_id=request.user.id).count()
            }
        response = render(request, 'df_goods/detail.html', result)
        goods_id = request.COOKIES.get('goods_id', None)
        if goods_id:
            goods_list_id = goods_id.split(',')
            if str(infos.id) not in goods_list_id:
                goods_list_id.insert(0, str(infos.id))
            else:
                goods_list_id.remove(str(infos.id))
                goods_list_id.insert(0, str(infos.id))
            if len(goods_list_id) > 5:
                goods_list_id.pop()
            goods_id = ','.join(goods_list_id)
        else:
            goods_id = str(infos.id)
            # this is dict
        response.set_cookie('goods_id', goods_id)
        return response