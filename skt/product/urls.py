from django.conf.urls import url
from .views import (
    ProductListView, ProductDetailView,
    ProductCommentView, ProductLikeView,
)

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^(?P<slug>[-\w]+)/add_comment/$', ProductCommentView.as_view(), name='product_create_comment_view'),
    url(r'^(?P<slug>[-\w]+)/add_like/$', ProductLikeView.as_view(), name='product_create_like_view'),
]