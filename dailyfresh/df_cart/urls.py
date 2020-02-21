from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.user_cart),
    url(r'^add(\d+)_(\d+)/$',views.add),
    url(r'^edit(\d+)_(\d+)/$',views.edit),
    url(r'^delete(\d+)/$',views.delete),
]
