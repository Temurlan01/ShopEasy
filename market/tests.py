from django.test import TestCase
from market.models import Product


class ProductTestCase(TestCase):

    def test_product_list_success(self):
        response = self.client.get('/products/')

        self.assertEqual(response.status_code, 200)


class ProductDetailTestCase(TestCase):

    def test_product_detail_success(self):

        product = Product.objects.create(
            name='Apple Watch 7',
            price=55000,
            description='хорошие часы',
            preview_image='/media/kakoy-nibud-file.jpeg'
        )

        response = self.client.get(f'/product_detail/{product.id}/')

        self.assertEqual(response.status_code, 200)

    def test_product_detail_not_found(self):
        response = self.client.get('/products/9999/')

        self.assertEqual(response.status_code, 404)
