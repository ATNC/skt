from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError

from .models import Product
from .forms import CommentForm


class ProductPageTest(TestCase):

    def create_product(self, name='Test name product',
                       description='Test description product', price=10.10,
                       slug='test-name-product'):
        return Product.objects.create(name=name, description=description, price=price, slug=slug)

    def test_product_creation(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))

    def test_unique_product_slug(self):
        product = self.create_product()
        with self.assertRaises(IntegrityError):
            product2 = self.create_product()

    def test_product_view(self):
        product = self.create_product()
        url_product_detail = reverse('product_detail', kwargs={'slug': product.slug})
        response = self.client.get(url_product_detail)
        self.assertEqual(response.status_code, 200)
        self.assertIn(product.name, response.content.decode('utf-8'))

    def test_comment_form(self):
        product = self.create_product()
        data = {'comment_text': 'texttexttext', 'to_product': product}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_comment_invalid(self):
        product = self.create_product()
        data = {'to_product': product}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())





