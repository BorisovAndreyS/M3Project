

from django.contrib.auth.views import LoginView
from django.urls import path


from products.views import ProductDetailView
from users import views

app_name = 'products'

urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name='product'),

]
