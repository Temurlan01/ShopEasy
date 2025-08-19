from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView
from market.models import Product
from users.models import CartItem


class HomeView(TemplateView):
    """Вью для отображение товаров в главной странице """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        product_list = Product.objects.all().order_by('-created_at')


        if user.is_authenticated:
            cart_count = user.cart_items.aggregate(
                total=Sum('quantity'))['total'] or 0
            favorite_count = user.favorite_products.count()

            cart_ids = list(user.cart_items.values_list(
                'product_id', flat=True)
            )
            favorite_ids = list(user.favorite_products.values_list(
                'id', flat=True)
            )
        else:
            cart_count = 0
            favorite_count = 0
            cart_ids = []
            favorite_ids = []
        context = {
            'product_list': product_list,
            'cart_count': cart_count,
            'favorite_count': favorite_count,
            'cart_ids': cart_ids,
            'favorite_ids': favorite_ids,
        }
        return context



class HomeSearchView(TemplateView):
    """Вью для поиска товаров """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        search_word = self.request.GET['search']
        if user.is_authenticated:
            cart_count = user.cart_items.aggregate(
                total=Sum('quantity'))['total'] or 0
            favorite_count = user.favorite_products.count()

            cart_ids = list(user.cart_items.values_list(
                'product_id', flat=True)
            )
            favorite_ids = list(user.favorite_products.values_list(
                'id', flat=True)
            )
        else:
            cart_count = 0
            favorite_count = 0
            cart_ids = []
            favorite_ids = []
        context = {
            'product_list': Product.objects.filter(
                Q(name__icontains=search_word) |
                Q(description__icontains=search_word),
            ),
            'cart_count': cart_count,
            'favorite_count': favorite_count,
            'cart_ids': cart_ids,
            'favorite_ids': favorite_ids,
        }
        return context



class ProductDetailView(TemplateView):
    """Вью для отображение детальной страницы товаров"""
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        try:
            product = Product.objects.get(slug=kwargs['slug'])
        except Product.DoesNotExist:
            raise Http404

        gallery_images = product.gallery.all()

        user = self.request.user
        if user.is_authenticated:
            cart_count = user.cart_items.aggregate(
                total=Sum('quantity'))['total'] or 0
            favorite_count = user.favorite_products.count()
            in_cart = user.cart_items.filter(product=product).exists()
            in_favorite = user.favorite_products.filter(id=product.id).exists()
        else:
            cart_count = 0
            favorite_count = 0
            in_cart = False
            in_favorite = False
        context = {
            'product': product,
            'gallery_image': gallery_images,
            'cart_count': cart_count,
            'favorite_count': favorite_count,
            'in_cart': in_cart,
            'in_favorite': in_favorite,
            'quantity_range': range(1, 11),
        }
        return context



class FavoriteProductListView(LoginRequiredMixin, TemplateView):
    """Получает список избранных товаров пользователя"""
    template_name = 'favorites.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {
            'favorite_products': user.favorite_products.all().
            order_by('-created_at')
        }
        return context



class AddProductToFavoriteView(View):
    """Добавляет товар в избранное пользователя"""
    template_name = 'favorites.html'

    def post(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
            product = get_object_or_404(Product, id=pk)
            user.favorite_products.add(product)
            user.save()
            return redirect('favorites-url')
        else:
            return render(request, 'login.html')



class RemoveProductToFavoriteView(View):
    """Удаляет товар из избранного пользователя"""
    template_name = 'favorites.html'

    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, id=pk)
        user.favorite_products.remove(product)
        user.save()

        return redirect('favorites-url')



class CartProductListView(LoginRequiredMixin, TemplateView):
    """Получает список товаров в корзине пользователя"""
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        cart_items = user.cart_items.select_related('product').all()
        for item in cart_items:
            item.total = item.product.price * item.quantity
        total_price = sum(item.total for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'quantity_range': range(1, 11),
        }
        return context



class AddProductToCartView(View):
    """Добавляет товар в корзину пользователя"""
    template_name = 'cart.html'

    def post(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
            product = get_object_or_404(Product, id=pk)
            quantity = int(request.POST.get('quantity', 1))
            cart_item, created = CartItem.objects.get_or_create(
                user=user, product=product
            )
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart-url')
        else:
            return render(request, 'login.html')



class UpdateCartItemView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart-url')



class RemoveProductToCartView(View):
    """Удаляет товар из корзины пользователя"""
    template_name = 'favorites.html'

    def post(self, request, pk):
        cart_item = get_object_or_404(
            CartItem, product_id=pk, user=request.user
        )
        cart_item.delete()
        return redirect('cart-url')

