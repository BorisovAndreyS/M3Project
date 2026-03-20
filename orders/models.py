from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
#Сама корзина у любого пользователя
class Cart(models.Model):
    # Обязательно User Как авторизованный так и анонимный
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='cart'
    )

    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        if self.user:
            return f'Cart for {self.user.email}'
        return f'Cart for session {self.session_key}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


#Элемент корзины
class CartItem(models.Model):
    #Связка с корзиной
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product') #Один товар в одной корзине


    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


    @property
    def total_price(self):
        #Цена за позицию с учетом колва
        return self.product.price * self.quantity
