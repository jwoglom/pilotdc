from django.conf.urls import patterns, include, url

import users
import dashboard
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webassess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'dashboard.views.dashboard_view', name='dashboard_view'),
    url(r'^login/$', 'users.views.process_login', name='process_login'),
    url(r'^logout/$', 'users.views.process_logout', name='process_logout'),
    url(r'^admin/$', 'users.views.admin_index', name='admin_index'),
)
