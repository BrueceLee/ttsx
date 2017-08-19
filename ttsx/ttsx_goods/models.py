# coding:utf-8

from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):

    ttitle = models.CharField(max_length='20')  # 名称
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')  # 选择商品类别时显示类别名称


class GoodsInfo(models.Model):

    gtitle = models.CharField(max_length='50')  # 名称
    gpic = models.ImageField(upload_to='goods')  # 图片
    gprice = models.DecimalField(max_digits=5, decimal_places=2)  # 价格999.99
    gclick = models.IntegerField(default=0)  # 点击量，用来进行人气排名
    gunit = models.CharField(max_length='20')  # 单位
    isDelete = models.BooleanField(default=False)
    gsubtitle = models.CharField(max_length='200')  # 副标题 商品名称下面的简单介绍
    gkucun = models.IntegerField(default=100)  # 库存
    gcontent = HTMLField()  # 商品详情
    gtype = models.ForeignKey('TypeInfo')  # 外键 商品所属类别



