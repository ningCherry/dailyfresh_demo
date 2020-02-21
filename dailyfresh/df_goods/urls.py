from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
    url(r'^(\d+)/$',views.detail),
    # url(r'^mysearch/$',views.mysearch),
    url(r'^search/$',views.MySearchView()),  #全文检索--自定义上下文
]
