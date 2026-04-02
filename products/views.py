from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, TemplateView, ListView
from .forms import ReviewsForm

from orders.models import CartItem
from orders.services import get_or_create_cart
from products.models import Product, Review, Category, ProductSpecification
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
        cart = get_or_create_cart(self.request)
        cart_item = CartItem.objects.filter(
            cart=cart,
            product=self.object
        ).first()
        context['quantity_in_cart'] = cart_item.quantity if cart_item else 0
        context['cart_item'] = cart_item
        context['specs'] = ProductSpecification.objects.filter(product=self.object)
        context['form'] = ReviewsForm()
        return context


class ProductListView(ListView):
    template_name = 'products/product-list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True) \
            .select_related('category') \
            .annotate(avg_rating=Avg('review__rating'))

        # filter by category_WORK
        categories = self.request.GET.get('category', None)
        if categories:
            qs = qs.filter(category__id__in=categories.split(','))

        # search
        to_search = self.request.GET.get('q', None)
        if to_search:
            qs = qs.filter(Q(name__icontains=to_search) | Q(description__icontains=to_search))

        qs_key = self.request.GET.get('sort', 'new')

        qs = qs.order_by(PRODUCT_QUERY_STRING_MAP[qs_key])

        return list(qs)

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)

        # Категории для слайдера
        context['categories'] = Category.objects.all()

        # Выбранные категории
        context['select_category'] = self.request.GET.getlist('category')

        # Текущая сортировка
        context['current_sort'] = self.request.GET.get('sort', 'new')

        # Сохраняем параметры GET без page
        context['get_params'] = self.request.GET.copy()
        if 'page' in context['get_params']:
            context['get_params'].pop('page')

        return context


class GuidesView(TemplateView):
    template_name = 'guides-recipes.html'


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    review = Review.objects.filter(product=product, user=request.user).first()
    if request.method == 'POST':
        form = ReviewsForm(request.POST, instance=review)  # Если есть редактируем
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:product', slug=product.slug)
        else:
            form = ReviewsForm(instance=review)
        return render(request, 'products/products-detail.html', {'form': form, 'product': product})
