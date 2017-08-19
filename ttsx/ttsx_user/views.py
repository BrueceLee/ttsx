# coding:utf-8
import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1

from ttsx_goods.models import GoodsInfo
from user_decorator import user_login
from ttsx_order.models import OrderMain

# Create your views here.


#注册
def register(request):

    context = {'title': '注册', 'top':'0'}
    return render(request, 'ttsx_user/register.html', context)


# 注册处理
def register_handle(request):

    '''

    # 方式1：
    # 接收数据
    post = request.POST

    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    umail = post.get('user_email')


    # 加密
    s1 = sha1()

    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()


    # 创建对象
    user = UserInfo()

    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()

    '''
    # 方式2：

    post = request.POST

    user = UserInfo()

    s1 = sha1()

    s1.update(post.get('user_pwd'))
    upwd_sha1 = s1.hexdigest()

    user.uname = post.get('user_name')
    user.upwd = upwd_sha1
    user.umail = post.get('user_email')
    user.save()

    # 完成后转向

    return redirect('/user/login')


# 注册验证用户名是否已存在
def register_valid(request):

    uname = request.GET.get('uname')
    result= UserInfo.objects.filter(uname=uname).count()
    context = {'valid':result}

    return JsonResponse(context)


# 登陆
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '登陆', 'uname':uname, 'top':'0'}
    return render(request, 'ttsx_user/login.html', context)


# 登陆处理
def login_handle(request):

    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    uname_jz = post.get('name_jz', '0')

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    context = {'tetle': '登陆', 'uname': uname, 'upwd': upwd}
    # print context,upwd_sha1 #for test
    # 根据用户名查询数据，如果未查到则返回[]，如果查到则返回[UserInfo]
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 0:
        # 用户名错误,添加错误标志
        context['name_error'] = '1'
        print 'name_error'
        return render(request, 'ttsx_user/login.html', context)

    else:
        if users[0].upwd == upwd_sha1:  # 登陆成功
            # 使用session记录当前登陆用户
            request.session['uid'] = users[0].id
            request.session['uname'] = uname
            path = request.session.get('url_path', '/')

            # print 'seccess' #for test
            response = redirect(path)

            if uname_jz == '1':

                response.set_cookie('uname', uname, expires= datetime.datetime.now()+datetime.timedelta(days=7))

            else:
                response.set_cookie('uname', '', max_age=-1)

            return response

        else:
            # 密码错误
            context['pwd_error'] = '1'
            # print 'pwd_error'   #for test

            return render(request, 'ttsx_user/login.html', context)


# 退出
def logout(request):

    request.session.flush()

    return redirect('/user/login/')


# 判断用户是否登陆
def islogin(request):

    result = 0
    if request.session.has_key('uid'):
        result = 1
    return JsonResponse({'islogin':result})


@user_login
def center(request):
    # 根据id查询已经登陆的用户。
    user = UserInfo.objects.get(pk=request.session['uid'])

    gids = request.COOKIES.get('goods_ids','0').split(',')

    gids.pop()  # 由于在用户没有浏览商品时，cookie中默认值为‘’，
                # 而空字符串在转换为十进制整数进行查询时间会出错，所以要把它删除掉。即删除最后一个元素。
    # print gids   # for test
    glist = []

    for gid in gids:

        glist.append(GoodsInfo.objects.get(id=gid))
    print glist
    context = {'title': '用户信息', 'user': user, 'glist':glist}
    return render(request, 'ttsx_user/center.html', context)


@user_login
def center_order(request):
    pindex = int(request.GET.get('pindex', '1'))
    # 查询当前用户所有订单，并进行分页
    uid = request.session.get('uid')
    order_list = OrderMain.objects.filter(user_id=uid).order_by('-order_date')
    paginator = Paginator(order_list,2)
    order_page = paginator.page(pindex)

    # 页码
    page_list = []
    if paginator.num_pages < 5:
        page_list = paginator.page_range
    elif order_page.number <= 2:
        page_list = range(1, 6)
    elif order_page.number >= paginator.num_pages - 1:
        page_list = range(paginator.num_pages - 4, paginator.num_pages + 1)
    else:
        page_list = range(pindex - 2, pindex + 3)

    context = {'title': '用户订单', 'order_page': order_page, 'page_list': page_list}

    return render(request, 'ttsx_user/center_order.html', context)


@user_login
def center_site(request):
    # 根据id查询已经登陆的用户。获取已经登陆的用户对象。
    user = UserInfo.objects.get(pk=request.session['uid'])

    if request.method == 'POST':

        post = request.POST

        user.ushou = post.get('ushou')
        user.uaddr = post.get('uaddr')
        user.umail = post.get('umail')
        user.uphone = post.get('uphone')
        user.save()

    context = {'title': '用户地址', 'user': user}

    return render(request, 'ttsx_user/center_site.html', context)

