from django.db import models
from user.models import UserProfile
from datetime import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.


# 订单
class Order(models.Model):
    o_id = models.CharField(max_length=100, primary_key=True, verbose_name='订单编号')
    o_date = models.DateTimeField(auto_now_add=True, verbose_name='订单日期')
    o_pay = models.BooleanField(choices=((True, '已支付'), (False, '未支付')), default=False, verbose_name='是否支付')
    o_total_price = models.CharField(max_length=100, verbose_name='总价')
    user = models.IntegerField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'df_order_orderinfo'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


# 商品种类
class Commodity_type(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='商品分类')
    class_name = models.CharField(max_length=50, null=True, verbose_name='商品种类')
    type_img = models.ImageField(verbose_name='商品种类图片', upload_to='images/type/%Y/%m/', default='')

    class Meta:
        db_table = 'df_goods_typeinfo'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 商品
class Commodity(models.Model):
    g_title = models.CharField(max_length=100, null=True, verbose_name='品种')
    g_pic = models.ImageField(upload_to='images/blog/%Y/%m/', default='images/blog/default.jpg', verbose_name='商品图片')
    # 整数位数和小数位数
    g_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='价格')
    g_unit = models.CharField(max_length=50, null=True, verbose_name='单位')
    # 点击数
    g_click = models.IntegerField(null=True, default='0', verbose_name='点击数')
    # 描述
    g_desc = models.CharField(max_length=50, verbose_name='商品描述')
    # 囤货
    g_stock = models.IntegerField(null=True, verbose_name='数量')
    content = UEditorField(
        null=True,
        verbose_name='介绍',
        width=700,
        height=400,
        toolbars='full',
    )
    g_type = models.IntegerField(null=True)
    g_type = models.ForeignKey(Commodity_type, on_delete=models.CASCADE, verbose_name='商品类型')

    class Meta:
        db_table = 'df_goods_goodinfo'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


# 订单详情
class Detailinfo(models.Model):
    count = models.IntegerField(null=True)
    order = models.IntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    goods = models.IntegerField(null=True)
    goods = models.ForeignKey(Commodity, on_delete=models.CASCADE, verbose_name='商品')

    class Meta:
        db_table = 'df_order_orderdetailinfo'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name


# 购物车
class ShoopCart(models.Model):
    count = models.IntegerField(null=True)
    user = models.IntegerField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    good = models.IntegerField(null=True)
    good = models.ForeignKey(Commodity, on_delete=models.CASCADE)

    class Meta:
        db_table = 'df_cart_cartinfo'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name





