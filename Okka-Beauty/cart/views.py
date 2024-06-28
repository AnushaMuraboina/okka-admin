from django.shortcuts import render,get_object_or_404,redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        print(cart)

        items = []
        item_totals = []
        sub_total = 0

        if cart is not None:
            # Get all cart items associated with the current user's cart
            cart_items = cart.cartitem_set.all()

            # Check stock for each cart item and calculate totals only for in-stock items
            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity

                if int(product.stock) > 0:
                    # In-stock item, calculate total amount and add to totals

                    if product.sale_price:
                        # Use special price for calculation if available
                        price = product.sale_price
                    else:
                        # Use regular price if there is no special price
                        price = product.regular_price

                    #Sub Total calculation of Cart products
                    sub_total += quantity * price

                    # Cart list Product data store
                    items.append({
                        'id':cart_item.id,
                        'product': product,
                        'quantity': quantity,
                        'price':price,
                        'total_amount': quantity * price,
                    })

        breadcrumbs = [
            {'text': 'Home', 'url': '/'},  # Link to the homepage
            {'text': 'Cart', 'url': f'/cart/'},  # Link to the category page
        ]

        context = {
            'cart': cart,
            'items': items,
            'item_totals': item_totals,
            'sub_total': sub_total,
            'is_empty': (cart is None or not items),
            'breadcrumbs': breadcrumbs,
        }
        return render(request, 'cart/cart.html', context)

    else:
        # User is anonymous, retrieve the cart details from the session
        if 'cart' in request.session:
            cart_data = request.session['cart']
            items = []
            item_totals = []
            sub_total = 0

            for item in cart_data:
                product = get_object_or_404(Product, id=item['product'])
                
                # Check if the product is in stock before adding to cart
                if int(product.stock) > 0:
                    quantity = item['quantity']

                    if product.sale_price:
                        # Use special price for calculation if available
                        price = product.sale_price
                    else:
                        # Use regular price if there is no special price
                        price = product.regular_price

                    items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_amount': quantity * price,
                        # 'special_price':product.special_price,
                    })
                    item_totals.append({
                        'product': product.id,
                        'total_amount': quantity * price,
                    })
                    sub_total += quantity * price
                else:
                    # Product is out of stock, display it without calculating total and tax
                    items.append({
                        'product': product,
                        'quantity': 0,  # Quantity is 0 for out-of-stock products
                        'total_amount': 0,
                    })

            cart = None
            print('items')
            print(items)
            breadcrumbs = [
                {'text': 'Home', 'url': '/'},  # Link to the homepage
                {'text': 'Cart', 'url': f'/cart/'},  # Link to the category page
            ]
            context = {
                'cart': cart,
                'items': items,
                'item_totals': item_totals,
                'sub_total': sub_total,
                'breadcrumbs': breadcrumbs,
                'is_empty': (cart is None or not items),
            }
            return render(request, 'cart/cart.html', context)

        else:
            # No cart details found in session
            items = []
            item_totals = []
            sub_total = 0
            cart = None

            breadcrumbs = [
                {'text': 'Home', 'url': '/'},  # Link to the homepage
                {'text': 'Cart', 'url': f'/cart/'},  # Link to the category page
            ]
            context = {
                'cart': cart,
                'items': items,
                'item_totals': item_totals,
                'sub_total': sub_total,
                'is_empty': (cart is None or items is None or not items or 'cart' not in request.session),
                'breadcrumbs': breadcrumbs,
            }
            print(context)
            return render(request, 'cart/cart.html')


@require_POST
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_to_cart(request, id):
    print("axios post function is work")
    if request.method == 'POST':
        data = json.loads(request.body)

        quantity = int(data.get('quantity'))
        print(quantity)
        print(type(quantity))
    
        if request.user.is_authenticated:

            # Get the user's cart or create a new one if it doesn't exist
            cart, created = Cart.objects.get_or_create(user=request.user)
            print(cart)
            # Get the product with the given ID
            product = get_object_or_404(Product, pk=id)
            print(product)

            # Get Whishlist item
            wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()
            print('Wishlist item available')
            print(wishlist_item)

            #check wishlist available or not
            if wishlist_item:
                print('wishlist Item available ')
                wishlist_item.delete()
                print('wishlist item succesfully deleted')
                                                                                                                    

            # Get the quantity of the product from the POST data
            
            # Get the cart item for the product or create a new one if it doesn't exist
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            print('cart_item', cart_item)
            # Update the cart item's quantity if it already exists
            if created:
                cart_item.quantity = quantity
                print(cart_item.quantity)
                cart_item.save()
                print('cart item created')
            else:
                cart_item.quantity += quantity
                cart_item.save()
                print('cart item Updated')
            # if not created:
            #     print('if condition work')
            #     print(quantity)
            #     cart_item.quantity += quantity
            #     cart_item.save()
            #     print("cart save")
            #     # response_data = {'success':True}
            return JsonResponse({'success':True}, status=200)
        
        else:
            # User is anonymous, store the cart details in the session
            print('cart store session function work')
            if 'cart' not in request.session:
                request.session['cart'] = []

            # product = get_object_or_404(products, pk=id)
            # print(product)
            cart = request.session['cart']
            print(cart)

            # Check if the product already exists in the cart session
            for item in cart:
                if item['product'] == id:
                    # Update the quantity of the existing product
                    item['quantity'] += quantity
                    break
                    
            else:
                # Add a new product entry to the cart session
                cart.append({
                    'product': id,
                    'quantity': quantity,
                })
            print(cart)
            request.session.modified = True
        
        return redirect('cart') 
    


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product_id = data.get('product_id')
        print(product_id)
        quantity = int(data.get('quantity'))
        print(quantity)

        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(cart)
        # Get the product with the given ID
        product = get_object_or_404(Product, pk=product_id)
        print(product)       

         # Get the cart item for the product or create a new one if it doesn't exist
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # Update the cart item's quantity if it already exists
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            print("cart save")

        response_data = {'success':True, 'newquantity' : cart_item.quantity}
        return JsonResponse(response_data, status=200)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_cart_item(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.delete()
        return redirect('cart')
    
    if 'cart' in request.session:
        del request.session['cart']
        return redirect('cart')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required
@require_POST
def remove_cart(request, cart_item_id):
    try:
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.delete()
        return JsonResponse({'status': 'success'})
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wishlist(request):
    wishlist=[]
    if request.user.is_authenticated:
        wishlist = WishlistItem.objects.filter(user=request.user)

    breadcrumbs = [
        {'text': 'Home', 'url': '/'},  # Link to the homepage
        {'text': 'whishlist', 'url': f'/cart/wishlist/'},  # Link to the category page
    ]
    context = {
        'whishlist':wishlist,
        'breadcrumbs':breadcrumbs,
    }
    return render(request, 'cart/wishlist.html', context)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()
    
    # Get Wishlist item in Cart
    cart_item = CartItem.objects.filter(cart__user=request.user, product=product)

    # Check if wishlist or cart item exists
    if cart_item:
        cart_item.delete()

    if wishlist_item:
        wishlist_item.delete()
        # Get the updated wishlist count
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    
        response_data = {
            'success': True,
            'added_to_wishlist': False,  # or False based on your logic
            'wishlist_count': wishlist_count  # Add this line to include the wishlist count in the response
        }
    else:
        WishlistItem.objects.create(user=request.user, product=product)

        # Get the updated wishlist count
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
        
        response_data = {
            'success': True,
            'added_to_wishlist': True,  # or False based on your logic
            'wishlist_count': wishlist_count  # Add this line to include the wishlist count in the response
        }

    return JsonResponse(response_data, status=200)

# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_wishlist_item(request, wishlist_item_id):
    wishlist_item = get_object_or_404(WishlistItem, pk=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_price_info(request):
    user = request.user
    print(user)
    sub_total = []
    
    if request.method == 'POST':     
        data = json.loads(request.body)  # Parse the JSON data sent in the request body

        sub_total = data.get('sub_total')
        print(sub_total)
        total_amount = data.get('total_amount')
        print(total_amount)
        print("cart is check out ")

        discount = data.get('discount')
        print('discount value ')
        print(discount)

        cartItems = data.get('cartItems')
        print(cartItems)

        request.session['sub_total'] = sub_total
        # request.session['tax'] = tax
        request.session['total_amount'] = total_amount
        request.session['cartItems'] = cartItems
        request.session['discount'] = discount
        return JsonResponse({'success': True})