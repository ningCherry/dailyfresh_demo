from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from df_cart.models import *

# Create your views here.

def index(request):
    # 查询各个分类的最新4条，最热4条数据
    typelist=TypeInfo.objects.all()  #获取所有商品种类
    type0=typelist[0].goodsinfo_set.order_by('-id')[0:4]  #按降序排序商品种类第一个下面的所有商品，取前四个
    type01=typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # 按照点击量
    type1=typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11=typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2=typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21=typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3=typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31=typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4=typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41=typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context={
        'title':'首页',
        'guest_cart':1,
        'cart_num':cart_count(request),
        'type0':type0,'type01': type01,
        'type1':type1,'type11': type11,
        'type2':type2,'type21': type21,
        'type3':type3,'type31': type31,
        'type4':type4,'type41': type41,
        'type5':type5,'type51': type51,
    }

    return render(request,'df_goods/index.html',context)


#统计购物车数量
def cart_count(request):
    cart_num = 0
    # 判断是否存在登录状态,统计购物车数量
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()
    return cart_num


def list(request,tid,pindex,sort):
    # tid：商品种类信息  pindex：商品页码 sort：商品显示分类方式
    typeinfo=TypeInfo.objects.get(pk=int(tid))   # 根据主键查找当前的商品分类  海鲜或者水果
    news=typeinfo.goodsinfo_set.order_by('-id')[0:2]  #list左侧最新商品推荐
    goods_list=[]   #中间栏商品显示方式

    if sort=='1':
        goods_list=typeinfo.goodsinfo_set.order_by('-id')
    elif sort=='2':
        goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    elif sort=='3':
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick')

    # 创建Paginator一个分页对象
    paginator=Paginator(goods_list,4)
    # 返回Page对象，包含商品信息
    page=paginator.page(int(pindex))
    context={
        'title':'商品列表',
        'guest_cart':1,
        'cart_num': cart_count(request),
        'page':page,
        'sort':sort,
        'news':news,
        'typeinfo':typeinfo,
    }
    return render(request,'df_goods/list.html',context)


def detail(request,gid):
    goods=GoodsInfo.objects.get(pk=int(gid))
    goods.gclick+=1  #商品点击量
    goods.save()

    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={
        'title':goods.gtype.ttitle,
        'guest_cart': 1,
        'cart_num': cart_count(request),
        'goods':goods,
        'news':news,
        'id':gid
    }
    response=render(request,'df_goods/detail.html',context)

    #-------记录最近浏览，在用户中心使用。关联见def_user/views.info模块
    goods_ids=request.COOKIES.get('goods_id','')
    # print(goods_ids)
    goods_id='%d'%goods.id  #获取商品id
    # 判读是否有浏览记录，如果有则继续判断
    if goods_ids!='':
        goods_ids1=goods_ids.split(',')   #拆分为列表
        if goods_ids1.count(goods_id) >= 1:  # 如果商品已经被记录，则先删除再记录
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)  # 添加到第一个
        # print(goods_ids1)
        if len(goods_ids1) >= 6:  #如果超过6个则删除最后一个
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)  #拼接为字符串
    else:
        goods_ids=goods_id   #如果没有浏览记录则直接加
        # print(goods_ids)
    response.set_cookie('goods_id',goods_ids)  #写入cookie

    return response


#全文检索+中文分词
def mysearch(request):
    return render(request,'df_goods/mysearch.html')


#全文检索--自定义上下文
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context=super(MySearchView,self).extra_context()
        context['title']='搜索'
        context['guest_cart']=1
        context['cart_num']=cart_count(self.request)
        return context