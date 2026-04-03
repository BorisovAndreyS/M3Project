from .models import Cart

#Функция возвращает корзину для текущего пользователя/сессии,
# Если ее нет, то создает
def get_or_create_cart(request):
    #Для авторизованных пользователей
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_key': None})
        print(cart.user, ' ', cart.session_key)

        if cart.session_key:
            cart.session_key = None
            cart.save()




        return cart

    # Для анонимных пользователей
    if not request.session.session_key:
        request.session.create() #Создали сессию если нету

    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key = session_key,
        defaults={'user': None}
    )

    if request.session.session_key:
        old_cart = Cart.objects.filter(
            session_key=request.session.session_key,
            user__isnull=True
        ).first()
        if old_cart and old_cart != cart:
            old_cart.items.update(cart=cart)
            old_cart.delete()

    return cart

# def get_cart(request):
#     # Для авторизованных пользователей
#     if request.user.is_authenticated:
#         cart = Cart.objects.get(
#             user=request.user,
#             defaults={'session_key': None})
#         return cart
#
#     if


