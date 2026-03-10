

from django.contrib.auth.views import LoginView
from django.urls import path


from products.views import ProductDetailView, ProductListView, GuidesView
from users import views

app_name = 'products'

urlpatterns = [
    path('guides-recipes/', GuidesView.as_view(), name= 'guides-recipes'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('', ProductListView.as_view(), name='products_list'),


]
