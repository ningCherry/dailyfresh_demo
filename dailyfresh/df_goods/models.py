from django.db import models
from tinymce.models import HTMLField    # 使用富文本编辑框要在settings文件中安装，配置app和url
# 将一对多的关系维护在GoodsInfo中维护，另外商品信息与分类信息都属于重要信息需要使用逻辑删除
# Create your models here.

class TypeInfo(models.Model):    #商品种类
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)   # 逻辑删除

class GoodsInfo(models.Model):    #商品详细信息
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='df_goods')   # 商品图片,要在settings文件设置路径
    gprice=models.DecimalField(max_digits=5,decimal_places=2)   # 商品价格小数位为两位，整数位为3位
    gunit=models.CharField(max_length=20,default='500g')
    gclick=models.IntegerField()   #点击率
    gjianjie=models.CharField(max_length=200)
    gkucun=models.IntegerField()
    gcontent=HTMLField()   #富文本编辑器
    isDelete=models.BooleanField(default=False)
    gtype=models.ForeignKey(TypeInfo,on_delete=models.CASCADE)  # 外键关联TypeInfo表
    # gadv=models.BooleanField(default=False)  #商品是否推荐
