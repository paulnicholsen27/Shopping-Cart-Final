from django.conf.urls import patterns, include, url
from ogstore2 import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('shoppingcart.views',
    url(r'^home/', 'homepage'),    
    url(r'^products/', 'products'),
    url(r'^productdetail/(?P<product_internal_id>\w+)/', 'detail'),
    url(r'^shoppingcart/', 'shoppingcart'),
    url(r'^checkout/', 'checkout'),
    url(r'^orderhistory/', 'orderhistory'),
    url(r'^createuser/', 'create_user'),
    url(r'^location/', 'location'),
    url(r'^logout/', 'log_out'),
    url(r'^changeuser/', 'changeuser'),

   
)
