# from config.urls import urlpatterns
from django.urls import path, include
from .views import add_to_cart, CartDetailView, update_cart_item

app_name = 'orders'
#
#
urlpatterns = [
    path('add/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('update/<int:itemid>/', update_cart_item, name='update_cart_item'),
]
#