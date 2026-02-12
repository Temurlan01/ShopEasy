from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ProductCategory(models.Model):
    title = models.CharField(max_length=150)


class Product(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(
        max_length=200, unique=True, blank=True,
        null=True, verbose_name='URL'
    )
    price = models.PositiveIntegerField(verbose_name='цена без скидки',
                                        help_text='в сомах'
                                        )

    description = models.TextField(verbose_name='Описание')
    preview_image = models.ImageField(upload_to='products_preview_images/',
                                      verbose_name='Изображение товара'
                                      )
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name='Количество'
                                           )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    """Модель галереи товара."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='gallery'
                                )
    image = models.ImageField(upload_to='product_gallery/')

    class Meta:
        verbose_name_plural = 'Галерея товаров'
        verbose_name = 'Галерея товара'


class ProductRating(models.Model):
    from users.models import CustomUser

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = 'Рейтинг товаров'
        verbose_name = 'Рейтинг товара'
        unique_together = ('user', 'product',)

