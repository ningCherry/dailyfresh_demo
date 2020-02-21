from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# Create your models here.

#谁买了几个什么
class CartInfo(models.Model):
    user=models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    goods=models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)
    count=models.IntegerField()