from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^\+admin/login$', 'cms.views.admin_login'),
    (r'^\+admin/logout$', 'cms.views.admin_logout'),
    (r'^\+admin/api$', 'cms.views.admin_api'),
    (r'^\+admin/navigation$', 'cms.views.admin_navigation'),
    (r'^\+admin/languages$', 'cms.views.admin_languages'),
    (r'^\+admin/pages$', 'cms.views.admin_list_pages'),
    (r'^\+admin/pages/(?P<page>[0-9]+)$', 'cms.views.admin_page_overview'),
    (r'^\+admin/pages/(?P<page>[0-9]+)/edit/(?P<lang>.+)$', 'cms.views.admin_page_edit'),
    (r'^\+admin/pages/(?P<page>[0-9]+)/locations$', 'cms.views.admin_page_locations'),
    (r'^\+admin/pages/(?P<page>[0-9]+)/statistics$', 'cms.views.admin_page_statistics'),
    (r'^\+admin$', 'cms.views.admin_index'),
    (r'^\+plugins/(?P<plugin>\w+)(?P<path>/.+)?', 'cms.views.plugin_handler'),
    (r'^(?P<path>.+)', 'cms.views.view'),
    (r'', 'django.views.defaults.page_not_found')
)
