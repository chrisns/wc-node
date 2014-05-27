from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()


# urlpatterns = patterns('',
#                       ('^_ah/warmup$', 'djangoappengine.views.warmup'),
#                       ('^$', 'django.views.generic.simple.direct_to_template',
#                        {'template': 'home.html'}),
#                       ('^admin/', include(admin.site.urls)),
#                        )
from django.conf.urls import patterns, include, url
from snippets import views
from executions import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
router.register(r'executions', views.ExecutionViewSet)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tutorial.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^', include(router.urls)),
                       # url(r'^', include('snippets.urls')),
                       # url(r'^admin/', include(admin.site.urls)),
                       )
