from django.conf.urls import url

import views as views

app_name = 'resizer'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^resizer_op/$', views.resizer_op, name='resizer_op'),
    url(r'^resize_op_fetch_param/$', views.resize_op_fetch_param, name='resize_op_fetch_param'),
    url(r'^compress_op/$',views.compress_op,name='compress_op'),
    url(r'^compress_op_fetch_param/$',views.compress_op_fetch_param,name='compress_op_fetch_param'),
    url(r'^enhance_op/$',views.enhance_op,name='enhance_op'),
    url(r'^enhance_op_fetch_param/$', views.enhance_op_fetch_param, name='enhance_op_fetch_param'),

]
