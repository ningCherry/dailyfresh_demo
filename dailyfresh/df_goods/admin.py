from django.contrib import admin
from .models import *

# Register your models here.
#注册模型类
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gunit','gclick','gprice','gpic','gkucun','gjianjie']

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)