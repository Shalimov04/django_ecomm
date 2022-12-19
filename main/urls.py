from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from website.urls import urlpatterns as website_urls
from api.urls import urlpatterns as api_urls
from main import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = "MyPC - панель администратора"
admin.site.site_title = "ADMIN"
admin.site.index_title = "Вы вошли в панель администратора!"

urlpatterns = website_urls + api_urls + staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
