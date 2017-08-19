from django.db import models

# Create your models here.

class CartInfo(models.Model):

    user = models.ForeignKey('ttsx_user.UserInfo')
    goods = models.ForeignKey('ttsx_goods.GoodsInfo')
    count = models.IntegerField()

    




