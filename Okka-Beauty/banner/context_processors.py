from .models import *
from product.models import *
from cart.models import *
from collections import defaultdict


def nav_context(request):
    user = request.user
    brands = Brand.objects.all().order_by('name')
    grouped_brands = {}

    for brand in brands:
        if brand.name:  # Ensure the name is not empty
            initial = brand.name[0].upper()
            if initial not in grouped_brands:
                grouped_brands[initial] = []
            grouped_brands[initial].append(brand)

    cart_count = 0
    cart_total = 0.00
    wish_count = 0
    user_profile = None
    subtotal = 0.00  # Initialize subtotal here
    cart_items = []

    if request.user.is_authenticated:
        user = request.user
        cart_count = CartItem.objects.filter(cart__user=user).count()
        cart = Cart.objects.filter(user=request.user).first()

        if cart is not None:
            cart_items = cart.cartitem_set.all()

            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity

                if int(product.stock) > 0:
                    if product.sale_price:
                        price = product.sale_price
                    else:
                        price = product.regular_price

                    cart_total += float(quantity * price)
                    subtotal = round(cart_total, 2)

        wish_count = WishlistItem.objects.filter(user=user).count()
    else:
        if 'cart' in request.session:
            cart_count = len(request.session['cart'])
        cart_items = []

    search_history = request.session.get('search_history', [])[:10]

    return {'grouped_brands': grouped_brands, 'cart_count': cart_count, 'wish_count': wish_count, 'search_history': search_history, 'cart_total': subtotal, 'cart_items': cart_items}
