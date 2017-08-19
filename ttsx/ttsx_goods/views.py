# coding:utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from models import *
from haystack.generic_views import SearchView


# Create your views here.


# 首页视图
def index(request):

    goods_list = [] # [{},{},{}]==> {'typeinfo':, "new_list':, 'click_list':}

    type_list = TypeInfo.objects.all()  # 包含所有的商品类别对象

    for t1 in type_list:

        nlist = t1.goodsinfo_set.order_by('-id')[0:4]  # 列表，保存最新的四个商品对象
        clist = t1.goodsinfo_set.order_by('-gclick')[0:4]  # 列表，保存最火的四个商品对象

        goods_list.append({'t1':t1, 'nlist':nlist, 'clist':clist})  # 把这些数据组成一个字典存储在goods_list列表中

    context = {'title':'首页', 'glist':goods_list, 'cart_show':'1'}

    return render(request, 'ttsx_goods/index.html', context)


# 列表页视图
def goods_list(request,tid,pindex,orderby):

    try:
        t1 = TypeInfo.objects.get(pk=int(tid))  # 获取当前分类对象

        new_list = t1.goodsinfo_set.order_by('-id')[0:2]

        order_str = '-id'
        desc = '1'
        if orderby == '2':

            desc = request.GET.get('desc','1')
            if desc == '1':
                order_str = '-gprice'
                # desc = '0'
            else:
                order_str = 'gprice'
                # desc = '1'

        elif orderby == '3':

            order_str = '-gclick'

        glist = t1.goodsinfo_set.order_by(order_str)  # 当前分类对象下的所有商品

        paginator = Paginator(glist,15)  # 显示方式是每页15个

        pindex1 = int(pindex)
        if pindex1 < 1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:  # num_pages表示最大页数
            pindex1 =paginator.num_pages

        page = paginator.page(pindex1)  # 显示第一页

        context = {'title':'列表页', 'cart_show':'1', 't1':t1, 'new_list':new_list, 'page':page, 'desc':desc, 'orderby':orderby}

        return render(request, 'ttsx_goods/list.html', context)
    except:

        return render(request, '404.html')


# 详细页视图
def detail(request,id):

    try:
        goods = GoodsInfo.objects.get(pk=int(id)) # get方法会产生异常 注意此处要把id转换成int型

        # 浏览商品后该商品点击量加1
        goods.gclick += 1
        goods.save()

        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

        context = {'title': '详情页', 'cart_show': '1', 'goods': goods, 'new_list': new_list}
        response = render(request, 'ttsx_goods/detail.html', context)

        # 存储5个最新浏览过的商品id

        # 读取cookie中已经保存的最近浏览商品信息
        gids = request.COOKIES.get('goods_ids','0').split(',') # 获取cookie中已保存的最新浏览商品id，该信息是字符串，用‘，’进行分割id。

        # 判断id是否已经在列表中，如果在，就先删除，再添加到最前面。
        if id in gids:
            gids.remove(id)  # 注意id是字符串所以不能加引号，否则会出错。

        gids.insert(0, id)  # 把最新浏览的商品的id插入到最前面。
        # 对列表进行判断，如果超过5个元素就删除最后一个元素。
        if len(gids) > 6 :

            gids.pop()

        response.set_cookie('goods_ids',','.join(gids),max_age=60*60*24*7)
        print gids
        return response

    except:

        return render(request,'404.html')


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['cart_show']='1'
        page_range=[]
        page=context.get('page_obj')
        if page.paginator.num_pages<5:
            page_range=page.paginator.page_range
        elif page.number<=2:#第1、2页
            page_range=range(1,6)
        elif page.number>=page.paginator.num_pages-1:#倒数第1、2页 6 7 8 9 10
            page_range=range(page.paginator.num_pages-4,page.paginator.num_pages+1)
        else:# 3 4 5 6 7
            page_range=range(page.number-2,page.number+3)
        context['page_range']=page_range
        return context

