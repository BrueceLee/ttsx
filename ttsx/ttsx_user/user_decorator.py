# coding:utf-8
from django.shortcuts import redirect


def user_login(func):
    def func1(request,*args,**kwargs):
        # 判断用户是否已经登陆
        # if request.session.get('uid'):
        if request.session.has_key('uid'):
            # 已经登陆，则调用被装饰的视图函数
            return func(request,*args,**kwargs)

        else:
            # 用户未登陆，重定向到登陆页
            return redirect('/user/login/')

    return func1



