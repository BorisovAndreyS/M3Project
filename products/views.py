from django.db.models import Avg, Q
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from products.models import Product, Review, Category
from config.settings import PRODUCT_QUERY_STRING_MAP


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
    # queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True) \
            .select_related('category') \
            .annotate(avg_rating=Avg('review__rating'))

        #filter by category
        categories = self.request.GET.get('categories', None)
        if categories:
            qs = qs.filter(category__slug__in = categories.split(','))


        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(Q(name__icontains=to_search) | Q(description__icontains=to_search))




        #sort
        qs_key = self.request.GET.get('sort', 'new')

        qs = qs.order_by(PRODUCT_QUERY_STRING_MAP[qs_key])
        # if sort == 'price':
        #     qs = qs.order_by('price')
        # elif sort == 'rating':
        #     qs = qs.order_by('-avg_rating')


        return list(qs)

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class GuidesView(TemplateView):
    template_name = 'guides-recipes.html'
