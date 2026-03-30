import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from orders.models import CartItem, Cart, Order, OrderItem
from orders.services import get_or_create_cart
from products.models import Product
from django.views.generic import DetailView, TemplateView, FormView
from .form import CheckoutForm


# Create your views here.
def update_cart_item(request, itemid):
    product_cart_itemid = CartItem.objects.get(id=itemid)
    product_stock_total = product_cart_itemid.product.stock
    quantity = product_cart_itemid.quantity
    cart = product_cart_itemid.cart
    # print(request.user.is_authenticated)
    is_ajax = request.content_type == 'application/json'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        target_quantity = int(data.get('quantity'))
        if target_quantity > product_stock_total:
            target_quantity = quantity
            return JsonResponse({
                'success': False,
                'message': f'Доступно только {product_cart_itemid.product.stock}',
                'quantity': target_quantity,
            })

        if target_quantity == 0:
            product_cart_itemid.delete()
            return JsonResponse({
                'success': True,
                'message': f'Позиция {product_cart_itemid} изменена в корзину',
                'quantity': target_quantity,
                'action': 'removed' if target_quantity == 0 else 'updated'
            })

        if request.user.is_authenticated:
            if cart.user == request.user:
                product_cart_itemid.quantity = target_quantity
                product_cart_itemid.save()
            else:
                print('Корзина не Ваша')
        else:
            if cart.session_key == request.session.session_key:
                product_cart_itemid.quantity = target_quantity
                product_cart_itemid.save()
            else:
                print('Корзина не ваша')

        # Если AJAX запрос - возвращаем JSON
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': f'Позиция {product_cart_itemid} изменена в корзину',
                'quantity': quantity,
                'action': 'removed' if target_quantity == 0 else 'updated'
            })


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True, )
    cart = get_or_create_cart(request)
    product_stock = product.stock

    is_ajax = request.content_type == 'application/json'

    if is_ajax:
        data = json.loads(request.body)
        target_quantity = int(data.get('quantity', 1))
    else:
        target_quantity = 1

    if target_quantity > product_stock:
        return JsonResponse({
            'success': False,
            'message': f'Доступно только {product.stock}',
            'quantity': target_quantity,
        })

    if target_quantity == 0:
        CartItem.objects.filter(cart=cart, product=product).delete()
        cart_item = None
        quantity = 0
    else:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': target_quantity}
        )
        if not created:
            cart_item.quantity = target_quantity
            cart_item.save()
        quantity = cart_item.quantity

    # Если AJAX запрос - возвращаем JSON
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': f'Товар {product.name} добавлен в корзину',
            'quantity': quantity,
            'action': 'removed' if target_quantity == 0 else 'updated'
        })
    # Если обычный запрос, редирект и сообщение
    messages.success(request, f'Товар {product.name} добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


class CartDetailView(TemplateView):
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cart = get_or_create_cart(self.request)
        context['cart'] = get_or_create_cart(self.request)

        return context


class CheckoutView(FormView):
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm  # или None для ручной обработки
    success_url = reverse_lazy('orders:order_success')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['phone'] = self.request.user.phone
        initial['city'] = self.request.user.city
        initial['address'] = self.request.user.address
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ← Добавить корзину в контекст для отображения состава
        context['cart'] = get_or_create_cart(self.request)
        return context

    def form_valid(self, form):
        # ← Логика создания заказа (см. Алгоритм выше)
        cart = get_or_create_cart(
            request=self.request
        )
        order = Order.objects.create(
            user=self.request.user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            # email=form.cleaned_data['email'],
            phone=form.cleaned_data['phone'],
            city=form.cleaned_data['city'],
            address=form.cleaned_data['address'],
            # total_price=cart.total_price
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )

        cart.items.all().delete()

        #Тут можно еще async отправка email

        return redirect('orders:order_success', id=order.id)


class CheckoutSuccessView(TemplateView):
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('id')
        context['order'] = get_object_or_404(Order, id=order_id)
        return context