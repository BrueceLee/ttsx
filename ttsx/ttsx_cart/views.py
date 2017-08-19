# coding:utf-8

from django.http import JsonResponse
from django.shortcuts import render
from models import CartInfo
from ttsx_user.user_decorator import user_login
from ttsx_user.models import UserInfo


# Create your views here.

# 向购物车中添加商品


def add(request):

    try:

        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count','1'))

        carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        if len(carts) == 1:
            cart = carts[0]
            cart.count += count
            cart.save()

        else:
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()

        return JsonResponse({'isadd':1})

    except:
        return JsonResponse({'isadd':0})


# 显示购物车中的商品数量
def count(request):

    uid = request.session.get('uid')
    # print uid
    cart_count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'cart_count':cart_count})


# 购物车主页
@user_login
def index(request):

    uid = request.session.get('uid')
    cart_list = CartInfo.objects.filter(user_id=uid)

    context = {'title':'购物车', 'cart_list':cart_list}


    return render(request, 'ttsx_cart/cart.html', context)


# 修改数据库中购物车数量
def edit(request):
    id = int(request.GET.get('id'))
    count = int(request.GET.get('count'))
    cart = CartInfo.objects.get(pk=id)
    cart.count = count
    cart.save()

    return JsonResponse({'ok':1})


# 删除购物车
def delete(request):
    id = int(request.GET.get('id'))
    cart = CartInfo.objects.get(pk=id)
    cart.delete()

    return JsonResponse({'ok':1})


# 订单
def order(request):
    user = UserInfo.objects.get(pk=request.session.get('uid'))
    cart_ids = request.POST.getlist('cart_id')  # cart_id有多个值，所以使用getlist。# 4,5,6
    cart_list = CartInfo.objects.filter(id__in=cart_ids)
    c_ids = ','.join(cart_ids)  # 4,5,6
    context = {'title':'订单','user':user, 'cart_list':cart_list, 'c_ids':c_ids}

    return render(request, 'ttsx_cart/order.html', context)






