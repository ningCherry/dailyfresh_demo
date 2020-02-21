from django.db import models
from df_goods.models import *
from df_cart.models import *

# Create your models here.

class OrderInfo(models.Model):  # 大订单
    oid=models.CharField(max_length=20,primary_key=True)  #大订单号
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)  #订单用户
    odate=models.DateTimeField(auto_now=True)  #时间
    oIsplay=models.BooleanField(default=False)  #是否支付
    ototal=models.DecimalField(max_digits=6,decimal_places=2)  # 虽然订单总价可以由多个商品的单价以及数量求得，但是由于用户订单的总价的大量使用，忽略total的冗余度
    oaddress=models.CharField(max_length=150)

# 无法实现：真实支付，物流信息
class OrderDetailInfo(models.Model):    # 大订单中的具体某一商品订单
    goods=models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)   # 关联商品信息
    order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE)   #订单
    price=models.DecimalField(max_digits=6,decimal_places=2)
    count=models.IntegerField()

