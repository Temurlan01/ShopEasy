from django.db import models
from django.contrib.auth.models import AbstractUser


from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """Кастомная модель для пользователей"""
    from market.models import Product

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        unique=True,
    )
    favorite_products = models.ManyToManyField(
        Product,
        related_name='favorite_users',
        blank=True,
    )
    cart_products = models.ManyToManyField(
        Product,
        related_name='cart_users',
        blank=True,
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'



class CartItem(models.Model):
    from market.models import Product

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='cart_items'
                             )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)