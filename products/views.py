from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from products.models import Product, Review, Category


# Create your views here.

class ProductDetailView(DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = Product
    template_name = 'products/products-detail.html'
    queryset = Product.objects.all().select_related('category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context

class ProductListView(ListView):
    template_name = 'products/product-list.html'
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'


    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
