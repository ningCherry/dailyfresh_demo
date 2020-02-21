"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^user/',include(('df_user.urls','user'),namespace='user')),  #namespace格式必须是这样的
    url(r'^tinymce/', include('tinymce.urls')), #富文本编辑器配置
    url(r'^',include('df_goods.urls')),
    url(r'^cart/',include(('df_cart.urls','cart'),namespace='cart')),
    url(r'^order/',include(('df_order.urls','df_order'),namespace='df_order')),
    # url(r'^search/', include('haystack.urls')),  #全文检索,注释了是为了在df_goods/urls定义url使用上下文全文检索
]
