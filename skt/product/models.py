import datetime
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class ProductCustomManager(models.Manager):

    def order_by_likes(self):
        return cache.get('products').annotate(likes_count=models.Count('product_likes')).order_by('-likes_count')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Product description')
    price = models.DecimalField(verbose_name='Product price', decimal_places=2, max_digits=5)
    created_at = models.DateTimeField(verbose_name='Created date', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='Modified date', auto_now=True)

    objects = ProductCustomManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def last_comments(self):
        latest_comments_date = datetime.datetime.now() - datetime.timedelta(days=1)
        return self.comments.filter(created_at__gt=latest_comments_date)

    @property
    def likes(self):
        return self.product_likes.count()

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        cache.set('products', Product.objects.all(), 3600)


class ProductComment(models.Model):

    class Meta:
        ordering = ['-created_at']

    to_product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='comments', verbose_name='To product'
                                   )
    comment_text = models.TextField(verbose_name='Product comment text')
    created_at = models.DateTimeField(verbose_name='Created date', auto_now_add=True)

    def __str__(self):
        return self.comment_text


class ProductLike(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user_likes', verbose_name='To user'
                                )
    to_product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_likes', verbose_name='To product'
                                   )



