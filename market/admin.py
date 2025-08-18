from django.contrib import admin
from django.utils.html import format_html
from market.models import Product, ProductGallery


class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag',)
    search_fields = ('name',)
    inlines = [ProductGalleryInlineAdmin]

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.preview_image.url))

    image_tag.short_description = 'Превью-изображение'







