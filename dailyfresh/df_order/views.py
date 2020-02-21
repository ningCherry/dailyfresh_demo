from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from df_user.models import *
from df_cart.models import *
from df_order.models import *

from df_user import user_decorator
from django.db import transaction   #事务

from datetime import datetime
from decimal import Decimal  #精确计算

@user_decorator.login
def order(request):
    uid=request.session['user_id']
    user=UserInfo.objects.get(id=uid)
    carts_id=request.GET.getlist('cart_id')  #获取url地址所有cart_id的值
    carts=[]
    total_price=0

    for goods_id in carts_id:
        cart=CartInfo.objects.get(id=goods_id)
        carts.append(cart)
        total_price+=float(cart.count)*float(cart.goods.gprice)

    total_price=float('%0.2f'%total_price)
    trans_count=10  #运费
    total_trans_price=total_price+trans_count

    context={
        'title':'订单',
        'page_name':1,
        'user':user,
        'carts':carts,
        'total_price':total_price,
        'trans_count':trans_count,
        'total_trans_price':total_trans_price,
    }
    return render(request,'df_order/place_order.html',context)


@user_decorator.login
@transaction.atomic()  #事务
def order_handle(requset):
    tran_id=transaction.savepoint()   # 创建保存点/保存事务发生点
    cart_ids=requset.POST.get('cart_ids')   # 用户提交的订单购物车，此时cart_ids为字符串，例如'1,2,3,'
    user_id=requset.session['user_id']   # 获取当前用户的id
    data1={}
    try:
        order_info=OrderInfo()    # 创建一个订单对象
        now=datetime.now()
        order_info.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),user_id)   # 订单号为订单提交时间和用户id的拼接
        order_info.odate=now   # 订单时间
        order_info.user_id=int(user_id)   # 订单的用户id
        order_info.ototal=Decimal(requset.POST.get('total'))   # 从前端获取的订单总价
        order_info.save()   # 保存订单

        for cart_id in cart_ids.split(','):    # 逐个对用户提交订单中的每类商品即每一个小购物车
            cart=CartInfo.objects.get(pk=cart_id)    # 从CartInfo表中获取小购物车对象
            order_detail=OrderDetailInfo()   # 大订单中的每一个小商品订单
            order_detail.order=order_info   # 外键关联，小订单与大订单绑定
            goods=cart.goods   # 具体商品
            if cart.count<goods.gkucun:   # 判断库存是否满足订单，如果满足，修改数据库
                goods.gkucun-=cart.count
                goods.save()
                order_detail.goods=goods
                order_detail.price=goods.gprice
                order_detail.count=cart.count
                order_detail.save()
                cart.delete()   # 并删除当前购物车
            else:    # 否则，则事务回滚，订单取消
                transaction.savepoint_rollback(tran_id)   #回滚到保存点
                return HttpResponse('库存不足')
        data1['ok']=1
        transaction.savepoint_commit(tran_id)   #提交从保存点到当前状态的所有数据库事务操作
    except Exception as e:
        print(e)
        print('未完成订单提交')
        transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
    return JsonResponse(data1)

