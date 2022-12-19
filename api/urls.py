import django.urls
from django.contrib import admin
from rest_framework.authtoken import views

from api import views as api_views

urlpatterns = [
    django.urls.path('admin/', admin.site.urls),
    django.urls.path('api/token_auth', views.obtain_auth_token),
    django.urls.path('api/validate', api_views.ValidateToken.as_view()),
    django.urls.path('api/pages', api_views.pages),
    django.urls.path('api/get_providers', api_views.GetProviders.as_view()),
    django.urls.path('api/get_batches', api_views.Batches.as_view()),
    django.urls.path('api/delete_batch/<int:pk>', api_views.delete),
    django.urls.path('api/add_batch', api_views.AddBatch.as_view()),
    django.urls.path('api/get_items', api_views.GetItems.as_view()),
    django.urls.path('api/get_orders', api_views.GetOrders.as_view()),
]
