from django.urls import path
from django.shortcuts import render
import website.views

urlpatterns = [
    path('', website.views.index),
    path('items/<int:cat_pk>/<str:cond_pk>/', website.views.all_items),
    path('item/<int:item_pk>/', website.views.item, name='item'),
    path('about', website.views.about),
    path('cart', website.views.cart, name='cart'),
    path('delete/<int:item_pk>/', website.views.delete, name='delete_item'),
    path('checkout', website.views.checkout, name='checkout'),
    path('order/<str:order_token>/', website.views.order, name='order'),
    path('kitten', website.views.cat),
]
