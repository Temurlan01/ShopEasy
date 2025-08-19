from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from market.views import (HomeView, CartProductListView, ProductDetailView,
FavoriteProductListView,AddProductToFavoriteView, RemoveProductToFavoriteView,
AddProductToCartView, RemoveProductToCartView, HomeSearchView,UpdateCartItemView
                          )
from orders.views import CreateOrderView,OrderSuccess
from users.views import (RegisterView, LoginView, MakeLoginView,
                         MakeRegisterView, MakeLogoutView
                         )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home-url'),
    path('home/search/', HomeSearchView.as_view(), name='home-search-url'),
    path('register/', RegisterView.as_view(), name='register-url'),
    path('login/', LoginView.as_view(), name='login-url'),
    path('make-login/', MakeLoginView.as_view(), name='make-login-url'),
    path('make-register/', MakeRegisterView.as_view(), name='make-register-url'),
    path('make-logout/', MakeLogoutView.as_view(), name='make-logout-url'),
    path('cart/', CartProductListView.as_view(), name='cart-url'),
    path('favorites/', FavoriteProductListView.as_view(), name='favorites-url'),
    path('add-product-to-favorite/<int:pk>/',
         AddProductToFavoriteView.as_view(),
         name='add-product-to-favorite-url'
         ),
    path('remove-product-to-favorite/<int:pk>/',
         RemoveProductToFavoriteView.as_view(),
         name='remove-favorite-url'
         ),
    path('product_detail/<slug:slug>/', ProductDetailView.as_view(),
         name='product-detail-url'
         ),
    path('add-product-to-cart/<int:pk>/', AddProductToCartView.as_view(),
         name='add-product-to-cart-url'
         ),
    path('update-cart-item/<int:pk>/', UpdateCartItemView.as_view(),
         name="update-cart-item-url"
         ),
    path('remove-product-to-cart/<int:pk>/', RemoveProductToCartView.as_view(),
         name='remove-cart-url'
         ),
    path('order/', CreateOrderView.as_view(), name='create-order-url'),
    path('order-success/', OrderSuccess.as_view(), name='order-success-url'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)