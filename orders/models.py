from django.db import models

from market.models import Product
from users.models import CustomUser




class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE,
                             related_name='orders'
                             )
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.TextField(verbose_name='Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создание заказа'
                                      )
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      verbose_name='Цена'
                                      )

    def __str__(self):
        return f"Заказ №{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE, verbose_name='Заказ'
                              )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт'
                                )
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена'
                                )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def total_price(self):
        return self.price * self.quantity


