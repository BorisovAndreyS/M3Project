import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from orders.models import CartItem, Cart
from orders.services import get_or_create_cart
from products.models import Product
from django.views.generic import DetailView, TemplateView


# Create your views here.
def update_cart_item(request, itemid):
    product_cart_itemid = CartItem.objects.get(id=itemid)
    cart = product_cart_itemid.cart
    print(request.user.is_authenticated)
    is_ajax = request.content_type == 'application/json'

    if request.method == 'POST' and is_ajax:
        data = json.loads(request.body)
        target_quantity = int(data.get('quantity'))

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


        quantity = product_cart_itemid.quantity
        # Если AJAX запрос - возвращаем JSON
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': f'Позиция {product_cart_itemid} изменена в корзину',
                'quantity': quantity,
                'action': 'removed' if target_quantity == 0 else 'updated'
            })

def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active = True, )
    cart = get_or_create_cart(request)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.content_type == 'application/json':
        data = json.loads(request.body)
        target_quantity = int(data.get('quantity', 1))
    else:
        target_quantity = 1

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

    #Если AJAX запрос - возвращаем JSON
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': f'Товар {product.name} добавлен в корзину',
            'quantity': quantity,
            'action': 'removed' if target_quantity == 0 else 'updated'
        })
    #Если обычный запрос, редирект и сообщение
    messages.success(request, f'Товар {product.name} добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

class CartDetailView(TemplateView):
    template_name = 'orders/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cart = get_or_create_cart(self.request)
        context['cart'] = get_or_create_cart(self.request)


        # context['cart_item'] =
        return context









