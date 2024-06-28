from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   
    path('cart/', views.cart, name="cart"),
    path('cart/add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_cart_item/<int:cart_item_id>', views.remove_cart_item, name = 'remove_cart_item'),
    path('remove_cart/<int:cart_item_id>', views.remove_cart, name = 'remove_cart'),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist_item/<int:wishlist_item_id>', views.remove_wishlist_item, name = 'remove_wishlist_item'),
    path('cart_price_info', views.cart_price_info, name='cart_price_info'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)