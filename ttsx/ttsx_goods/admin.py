# coding:utf-8

from django.contrib import admin
from models import *


# Register your models here.


#自定义管理器

class TypeAdmin(admin.ModelAdmin):

    list_display = ['id', 'ttitle']


class GoodsAdmin(admin.ModelAdmin):

    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gkucun']
    list_per_page = 15


# 注册模型

admin.site.register(TypeInfo,TypeAdmin)

admin.site.register(GoodsInfo,GoodsAdmin)



