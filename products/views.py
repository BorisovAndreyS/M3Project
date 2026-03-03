from django.shortcuts import render
from django.views.generic import DetailView
from products.models import Product, Review


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