# coding:utf-8

from datetime import datetime
from django.db import transaction
from django.shortcuts import render, redirect
from models import *
from ttsx_cart.models import CartInfo

# Create your views here.

'''
1.创建订单主表
2.接收购物车请求
3.查询到购物车请求信息
4.判断每个商品库存是否充足
5.如果充足：
    5.1创建订单详单
    5.2修改库存
    5.3删除购物车数据
    5.4删除购物车对象
6.如果库存不足，则放弃之前的所有操作，转向到购物车页面

'''


@transaction.atomic
def do_order(request):
    isok = True
    sid = transaction.savepoint()
    try:
        uid = request.session.get('uid')

        # 1
        now_str = datetime.now().strftime('%Y%m%d%H%M%S')
        main = OrderMain()
        main.order_id = '%s%d'%(now_str,uid)
        main.user_id = uid
        main.save()

        #2
        cart_ids = request.POST.get('cart_ids').split(',')  # '4,6,5'
        # 3
        cart_list = CartInfo.objects.filter(id__in=cart_ids)
        total = 0
        for cart in cart_list:  # 4
            if cart.count <= cart.goods.gkucun:  # 5
                # 5.1
                detail = OrderDetail()
                detail.order = main
                detail.goods = cart.goods
                detail.count = cart.count
                detail.price = cart.goods.gprice
                detail.save()
                # 5.2
                cart.goods.gkucun -= cart.count
                cart.goods.save()
                # 5.3
                total += cart.count * cart.goods.gprice
                main.total = total
                main.save()
                # 5.4
                cart.delete()
            else:  # 6
                isok = False
                transaction.savepoint_rollback(sid)
                break
        if isok:
            transaction.savepoint_commit(sid)

    except:
        transaction.savepoint_rollback(sid)
        isok = False

    if isok:
        return redirect('/user/center_order/')

    else:
        return redirect('/cart/')
