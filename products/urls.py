

from django.contrib.auth.views import LoginView
from django.urls import path


from products.views import ProductDetailView, ProductListView, GuidesView, add_review
from users import views

app_name = 'products'

urlpatterns = [
    path('guides-recipes/', GuidesView.as_view(), name= 'guides-recipes'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('', ProductListView.as_view(), name='products_list'),
    path('products/<slug:slug>/review', add_review, name='add_review'),


]
