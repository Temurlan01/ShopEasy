from django.db import models


class Product(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True,
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


class ProductGallery(models.Model):
    """Модель галереи товара."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='gallery'
                                )
    image = models.ImageField(upload_to='product_gallery/')

    class Meta:
        verbose_name_plural = 'Галерея товаров'
        verbose_name = 'Галерея товара'
