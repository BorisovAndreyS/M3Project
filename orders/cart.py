# from products.models import Product
#
#
# class Cart:
#     SESSION_KEY = 'cart'
#
#
#
#     def __init__(self, request):
#         self.session = request.session
#         self.cart = self.session.get(self.SESSION_KEY, {})
#
#
#     def change_quantity(self, product_slug:str, quantity:int):
#         self.cart
#
#     def add(self, product_slug:int):
#         product = Product.objects.get(slug=product_slug)
#         if product_slug not in self.cart:
#             self.cart[product_slug] = {'quatity': 0, 'price': product.price}
#         self.change_quantity(product_slug, 1)
#
#
#     def remove(self, product_slug:str):
#         self.change_quantity(product_slug, 1)
#
#
#     def clean(self):
#         pass