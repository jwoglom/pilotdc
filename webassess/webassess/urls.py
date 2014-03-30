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
    #url(r'^test/<number>/', 'quest.views.test', name='Test interface'),
    url(r'^dashboard/$', 'dashboard.views.dashboard_view', name='dashboard_view'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html',}),
    url(r'^logout/$', 'users.views.process_logout', name='process_logout'),
    url(r'^quest/take/(?P<test_id>\d+)$', 'quest.views.take_view', name='quest_take'),
    url(r'^quest/submit/$', 'quest.views.submit_view', name='Submit test'),
    url(r'^dashboard/teacher/$', 'dashboard.views.teacher_view', name='teacher_dashboard'),
    url(r'^quest/add/$', 'quest.views.add_view', name='add_view'),
    url(r'^quest/add/submit/$', 'quest.views.add_submit', name='add_submit'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
)
