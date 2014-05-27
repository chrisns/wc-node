from django.conf.urls.defaults import url
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import patterns

from . import views


# urlpatterns = patterns(
#     '',
#     url(r'^', include('executions.urls')),

    # url(r'^/api/product/$', views.ProductView.as_view(), name='product_view'),
# )
urlpatterns = patterns('executions.views',
                       url(r'^executions/$', views.ProductView.as_view()),
                       # url(r'^executions/(?P<pk>[0-9]+)/$',
                       #     'executions_detail'),
                       )
