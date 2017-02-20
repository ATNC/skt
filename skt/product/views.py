from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect

from .models import Product, ProductComment, ProductLike
from .forms import CommentForm


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        order_by = self.request.GET.get('order_by_like', None)
        if not cache.get('products'):
            cache.set('products', Product.objects.all(), 3600)
        if order_by:
            return Product.objects.order_by_likes()
        return cache.get('products')


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class ProductCommentView(CreateView):
    model = ProductComment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.kwargs.get('slug')})

    def form_valid(self, form):
        form.instance.to_product_id = self.request.POST.get('to_product_id')
        messages.add_message(self.request, messages.SUCCESS, 'Comment added successfully')
        return super(ProductCommentView, self).form_valid(form)


class PermissionView(CreateView):

    def _set_error_message(self, body_message):
        messages.add_message(self.request, messages.ERROR, body_message)

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        product_id = self.request.POST.get('product_id')
        reverse_link = reverse('product_detail', kwargs={'slug': self.kwargs.get('slug')})
        if user.is_anonymous:
            self._set_error_message('Only registered user')
            return HttpResponseRedirect(reverse_link)
        if ProductLike.objects.filter(to_user=user, to_product_id=product_id).exists():
            self._set_error_message('You can do like only one time')
            return HttpResponseRedirect(reverse_link)
        return super(PermissionView, self).dispatch(*args, **kwargs)


class ProductLikeView(PermissionView):
    model = ProductLike
    fields = []

    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.kwargs.get('slug')})

    def form_valid(self, form):
        user = self.request.user
        form.instance.to_product_id = self.request.POST.get('product_id')
        form.instance.to_user = user
        messages.add_message(self.request, messages.SUCCESS, 'Like added successfully')
        return super(ProductLikeView, self).form_valid(form)

