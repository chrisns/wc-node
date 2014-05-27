from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer
from rest_framework.routers import DefaultRouter

handler500 = 'djangotoolbox.errorviews.server_error'

dbindexer.autodiscover()
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls import patterns
from snippets import views
# from executions import views as execution_view


router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
# router.register(r'executions', execution_view.ExecutionView)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^', include('executions.urls')),

                       )
