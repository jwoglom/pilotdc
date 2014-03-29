from django.conf.urls import patterns, include, url

from users import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webassess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.process_login, name='process_login'),
    url(r'^logout/$', views.process_logout, name='process_logout'),
    url(r'^admin/$', views.admin_index, name='admin_index'),
)
