from django.shortcuts import render
from django.urls import reverse
from .models import *
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.cache import never_cache, cache_control
import json
from datetime import datetime, date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import mark_safe

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

@login_required(login_url='/login/?next=/checkout/')
def checkout(request):
    user = request.user
    try:
        billing_address = Address.objects.get(user=user, address_type='Billing')
    except Address.DoesNotExist:
        billing_address = None

    try:
        shipping_address = Address.objects.get(user=user, address_type='Shipping')
    except Address.DoesNotExist:
        shipping_address = None

    cart = Cart.objects.filter(user=user).first()
    if cart:
        items = cart.cartitem_set.filter(product__stock__gt=0, product__in_stock='Instock')
        item_details = []

        for item in items:
            product = item.product

            if product.sale_price:
                price = product.sale_price
            else:
                price = product.price

            item_details.append({
                'id':product.id,
                'product_name': product.name,
                'quantity': item.quantity,
                'price': price,
            })
    else:
        item_details = []

    sub_total = request.session.get('sub_total', 0)
    ship_cost = request.session.get('ship_cost', 0)
    coupon_status1 = request.session.get('coupon_status1', '')
    total_amount = request.session.get('total_amount', 0)
    coupon_code = request.session.get('coupon_code', '')

    context = {
        'billing_address': billing_address,
        'shipping_address': shipping_address,
        'items': item_details,
        'sub_total': sub_total,
        'ship_cost': ship_cost,
        'coupon_status1': coupon_status1,
        'total_amount': total_amount,
        'coupon_code': coupon_code,
    }

    return render(request, 'checkout/checkout.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def order(request, product_id=None):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        cart_items = data.get('cartItems')
        shipping_info_id = data.get('shipping_info')
        billing_info_id = data.get('billing_info')
        total_amount = data.get('total_amount', '0')
        tax_amount = data.get('tax_amount', '0')
        sub_tot = data.get('amount', '0')
        shipping_cost = data.get('shipping_cost', '0')
        discount = data.get('discount', '0')

        payment = 'Cash On Delivery'
        coupon_code = data.get('coupon_code')
        order_date = datetime.now().strftime('%d.%m.%y %H:%M:%S')

        # Fetch the Address instances from the provided IDs
        try:
            billing_address = Address.objects.get(id=billing_info_id)
            shipping_address = Address.objects.get(id=shipping_info_id)
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid address ID'})

        for item in cart_items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            product = Product.objects.get(id=product_id)
            total = item.get('total_amount', '0')

            product_quantity = Product.objects.get(id=product_id)

            if int(quantity) <= int(product_quantity.stock):
                order = Order.objects.create(
                    user=user,
                    billing_address=billing_address,
                    shipping_address=shipping_address,
                    amount=Decimal(sub_tot) if sub_tot else Decimal('0.00'),
                    disc_price=Decimal(discount) if discount else Decimal('0.00'),
                    tax_amount=Decimal(tax_amount) if tax_amount else Decimal('0.00'),
                    bill_amount=Decimal(total_amount) if total_amount else Decimal('0.00'),
                    shipping_cost=Decimal(shipping_cost) if shipping_cost else Decimal('0.00'),
                    payment_method='cash',
                    order_status="pending",
                )

                order_id = order.id

                for item in cart_items:
                    product_id = item.get('id')
                    quantity = item.get('quantity')
                    product = Product.objects.get(id=product_id)
                    name = product.name
                    total = item.get('total_amount', '0')

                    order_item = OrderItem.objects.create(
                        order=order,
                        product_id=product,
                        product_name=name,
                        price=product.regular_price,
                        quantity=quantity,
                        total=Decimal(total) if total else Decimal('0.00'),
                    )

                    if 'buy_now_data' in request.session:
                        buy_now_data = request.session.get('buy_now_data', {})
                        if product_id in buy_now_data:
                            del buy_now_data[product_id]
                            request.session['buy_now_data'] = buy_now_data
                            request.session.modified = True

                # if coupon_code:
                #     try:
                #         coupon_val = Coupon.objects.get(code=coupon_code)
                #         CouponUsage.objects.get_or_create(coupon=coupon_val, user=request.user)
                #     except ObjectDoesNotExist:
                #         pass

                invoice_id = f"{order_id}-INV"
                invoice_date = date.today()
                invoice = Invoice.objects.create(
                    invoice_id=invoice_id,
                    invoice_date=invoice_date,
                    user=user,
                    order=order,
                )

                item_count = OrderItem.objects.filter(order_id=order.id).count()
                print(item_count)

                # Send confirmation email
                email_subject = 'Your Alsuwaidi in  Order #{} of {} item'.format(order.order_id, item_count) 

                current_site = get_current_site(request)
                site_url = f"https://{current_site.domain}"
                print(site_url)
                
                # track_url = reverse('order_tracking', kwargs={'order_id': order_id})
                # invoice_url = reverse('download_invoice', kwargs={'order_id': order.id, 'invoice_id': invoice_id})

                # order_track = f"{site_url}{track_url}"
                # order_invoice = f"{site_url}{invoice_url}"

                # print(order_track)
                # print(order_invoice)

                print(order_item )
                email_body = render_to_string('email/order/order_process.html', {
                    'order': order,
                    'order_item':OrderItem.objects.filter(order_id=order.id),
                    'user': user,
                    'order_id': order_item.order_id,
                    'shippingaddress': Address.objects.get(id=order.shipping_address.id),
                    'billingaddress': Address.objects.get(id=order.billing_address.id),
                    'payment': order.payment_method,
                    'iteam_total': order.amount,
                    'tax':order.tax_amount,
                    'disc_price':order.disc_price,
                    'total':order.bill_amount,
                    # 'product_details': products.objects.filter(product_name=order_item.product_id),
                    'order_date':order.order_date,
                    'site_url':site_url,
                    # 'order_track':order_track,
                    # 'order_invoice':order_invoice,
                    
                })
                # print(order_item.product_id.get_absolute_url())
                # print(order_item.product_id__product_sku)      
                safe_email_body = mark_safe(email_body)
                email = EmailMultiAlternatives(
                email_subject, 
                body=safe_email_body, 
                from_email='onlineorders@suwaidillc.ae', 
                to=[user.email],
                )   
                email.attach_alternative(safe_email_body, "text/html")


                # Send email to admin
                admin_email = settings.ADMIN_EMAIL
                cc_email = settings.CC_EMAIL
                # admin_subject = 'New Order Received'
                admin_subject = f"New order received from {user.username}. Order ID: {order.order_id}"
                
                admin_email_body = render_to_string('email/order/order_process.html', {
                    'order': order,
                    'order_item':OrderItem.objects.filter(order_id=order.id),
                    'user': user,
                    'order_id': order_item.order_id,
                    'shippingaddress': Address.objects.get(id=order.shipping_address.id),
                    'billingaddress': Address.objects.get(id=order.billing_address.id),
                    'payment': order.payment_method,
                    'iteam_total': order.amount,
                    'tax':order.tax_amount,
                    'disc_price':order.disc_price,
                    'total':order.bill_amount,
                    # 'product_details': products.objects.filter(product_name=order_item.product_id),
                    'order_date':order.order_date,
                    'site_url':site_url,
                    # 'order_track':order_track,
                    # 'order_invoice':order_invoice,
                })
                safe_admin_email_body = mark_safe(admin_email_body)
                admin_email = EmailMultiAlternatives(
                    admin_subject,
                    safe_admin_email_body,
                    from_email='onlineorders@suwaidillc.ae',
                    to=[admin_email],
                    cc=cc_email,
                )
                admin_email.attach_alternative(safe_admin_email_body, "text/html")
                admin_email.send()


                email.send()
                print("email send to user and Admin")
                # generate_invoice_url = reverse("generate_invoice", args=[order_id])
                # print("url generate is work")
                # print(generate_invoice_url)

               

                # Generate and send the invoice email
                # email_subject = 'Invoice - {}'.format(invoice.invoice_id)
                # email_body = render_to_string('invoice_email.html', {
                #     'invoice': invoice,
                #     # Add any other required invoice details
                # })
                # safe_email_body = mark_safe(email_body)
                # email = EmailMultiAlternatives(
                #     email_subject,
                #     body=safe_email_body,
                #     from_email='marthal.zinavo@gmail.com',
                #     to=[user.email],
                # )
                # email.attach_alternative(safe_email_body, "text/html")
                # email.send()

                # if product_id:
                #     print('Product ID is available, so only delete cart items with product_id')
                #     CartItem.objects.filter(cart__user=user, product__id=product_id).delete()
                #     print("Cart items with product_id={} successfully deleted".format(product_id))
                #     # print('product id is available so only delete product_id available cart valu only')
                #     # Cart.objects.filter(user=user, products=product_id).delete()
                #     # print("Cart items with product_id={} successfully deleted".format(product_id))
                # else:
                #     print('all cart value is deleted')
                #     Cart.objects.filter(user=user).delete()
                #     print("cart sucessfully deleted")
                
                data = {
                    'success': True,
                    'order_id':order_id,
                }
                print(data)
                return JsonResponse(data, safe=False)

            else:
                print("quantity not available")
                response_data = {'success': False}
                return JsonResponse(response_data)
    else:
        print("Post function is not work ")
        response_data = {
            'success': False,
        }
        return JsonResponse(response_data)