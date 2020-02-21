from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
import hashlib
from . import user_decorator
from df_goods.models import *
from df_cart.models import *
from df_order.models import *
from django.core.paginator import Paginator

#-----------------------注册------------------------
def register(request):
    return render(request,'df_user/register.html',{'title':'注册'})

def register_handle(request):
    #接收用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd1=post.get('cpwd')
    uemail=post.get('email')
    #判断两次密码
    if upwd!=upwd1:
        return redirect('/user/register')
    #密码加密
    m=hashlib.md5()
    m.update(upwd.encode('utf-8'))
    mpwd=m.hexdigest()
    #创建对象,保存数据至数据库
    user=UserInfo()
    user.uname=uname
    user.upwd=mpwd
    user.uemail=uemail
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login')

def register_exit(requset):   #获取注册页用户名输入框的值的数量
    uname=requset.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


#-----------------------登录------------------------
def login(request):
    uname=request.COOKIES.get('uname')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    # return render(request,'df_user/login1.html',context)
    return render(request,'df_user/login.html',context)


###########方法一：没有利用ajax提交表单
def login_handle(request):
    #接受请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)  #没找到jizhu的值，则默认返回0
    #根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)  #返回的是个列表[]
    #判断：如果未查到则用户名错，如果查到则判断用户名是否正确，正确则转到用户中心
    if len(users)==1:
        m = hashlib.md5()
        m.update(upwd.encode('utf-8'))
        if m.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')  #获取相关页面登录时cookies存储的路径url。详见user_decorator.login模块，为了从哪个页面进就从哪个页面出
            red=HttpResponseRedirect(url)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname','',max_age=-1)  # 设置过期cookie时间，max_age=-1立刻过期
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red     #用户名和密码正确，重定向到用户中心
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname,'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


###########方法二：花了好长时间，写了下面这么多代码。只是自己做练习写的。就用方法一挺好，代码简洁
def login_handle1(request):
    # 接受请求信息
    post = request.POST
    uname = post.get('username')
    jizhu = post.get('jizhu', 0)  # 没找到jizhu的值，则默认返回0
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)  # 返回的是个列表[]
    red=HttpResponseRedirect('/user/info')
    if jizhu != 0:
        red.set_cookie('uname', uname)
    else:
        red.set_cookie('uname', '', max_age=-1)  # max_age=-1马上过期
    request.session['user_id'] = users[0].id
    request.session['user_name'] = uname
    return red

def user_exit(requset):     #这里除了用$.get()方法传递数据，还可以用$.post()方式传递数据，待研究
    uname = requset.GET.get('uname') #获取页面填写时的用户名
    # print(uname)
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})

def upwd_exit(requset):
    uname = requset.GET.get('uname')
    upwd=requset.GET.get('upwd')  #获取页面填写时写的密码
    print(upwd)
    m = hashlib.md5()
    m.update(upwd.encode('utf-8'))
    upwd1=m.hexdigest()
    user = UserInfo.objects.filter(uname=uname)  #返回的是个列表[]
    print(user)
    pwd=user[0].upwd
    if upwd1==pwd:
        count=1
    else:
        count=0
    return JsonResponse({'count': count})


#-----------------------用户中心------------------------
@user_decorator.login   #装饰器判断用户是否登录
def info(requset):
    uemail=UserInfo.objects.get(id=requset.session['user_id']).uemail

    # #--------最近浏览，关联见def_goods/views.detail模块
    goods_ids=requset.COOKIES.get('goods_id','1')   #####这里如果没有浏览记录goods_id，不给一个默认值的话会报错。有时间可以研究下怎么处理这种情况####
    # print(goods_ids)
    goods_ids1=goods_ids.split(',')
    # GoodsInfo.objects.filter(id__in=goods_ids)  #这样得到的数据没有按添加顺序排序，而是按id排序的
    goods_list=[]

    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    print(goods_list)

    context={'title':'用户中心',
             'page_name': 1,    #page_name用处，见base.html文件{% if page_name == 1 %}语句
             'uemail':uemail,
             'uname':requset.session['user_name'],
             'goods_list':goods_list
             }
    return render(requset,'df_user/user_center_info.html',context)


@user_decorator.login
def order(request,index):
    user_id=request.session['user_id']
    orders_list=OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    # print(orders_list)
    paginator=Paginator(orders_list,2)
    page=paginator.page(int(index))
    context = {
        'title': "用户中心",
        'page_name': 1,
        'page':page,
        'paginator':paginator,
        # 'orders_list':orders_list
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login   #装饰器判断用户是否登录
def site(requset):
    user=UserInfo.objects.get(id=requset.session['user_id'])
    if requset.method=='POST':
        post=requset.POST
        user.ushou=post.get('ushou')
        user.uadress=post.get('uadress')
        user.upostal=post.get('upostal')
        user.uphone=post.get('uphone')
        user.save()
    context={'user':user,'title':'用户中心','page_name': 1}
    return render(requset,'df_user/user_center_site.html',context)


#-----------------------登出------------------------
def logout(request):
    request.session.flush()    #删除当前的会话数据并删除会话的Cookie
    return redirect("/")    #？？？？这里为什么不能重定向到首页，我表示很困惑？？？？？？