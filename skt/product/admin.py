from django.contrib import admin
from .models import Product, ProductComment, ProductLike


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment)
admin.site.register(ProductLike)
