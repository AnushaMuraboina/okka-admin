from django.shortcuts import render,redirect
from .models import *
from banner.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.sessions.models import Session
from .forms import *
from checkout.models import *

from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.http import JsonResponse
import json

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from rating.models import *

# Create your views here.

# User Register Function
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Send welcome email using template
                subject = 'Welcome to Our Website'
                from_email = 'marthal.zinavo@gmail.com'
                recipient_list = [user.email]
                context = {'username': username}
                
                # Render the email template
                html_content = render_to_string('email/account_creation.html', context)
                
                # Create the email
                email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
                email.attach_alternative(html_content, "text/html")
                email.send()
                
                return redirect('home')  # Replace with your success URL
    else:
        form = SignUpForm()
    return render(request, 'base/login.html', {'form': form})

# User Login Function
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired success page
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'base/login.html')

# User Logout Function
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sign_out(request):
    logout(request)
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    if 'sessionid' in request.COOKIES:
        response.delete_cookie('sessionid')

    return response


# Home Page Function
def home(request):

    main_banner = MainBanner.objects.filter(active = True).order_by('slot_position')
    
    trending_banner = TrendingBrand.objects.filter(active = True).order_by('slot_position')

    price_banner = PriceBanner.objects.filter(active = True).order_by('slot_position')
    
    foot_banner = FooterBanner.objects.filter(active = True).order_by('slot_position')

    skin_routine = SubCategory.objects.filter(skin_routine=True).order_by('slot_position')

    Why_Us = WhyUs.objects.filter(active = True).order_by('slot_position')
 
    # latest_beauty_product = Product.objects.filter(categories__name='BEAUTY').order_by('-created_at')
    # print(latest_beauty_product)

    # Check if 'new_arrivals' is checked
    new_arrivals_checked = request.GET.get('new_arrivals', False)

    if new_arrivals_checked:
        latest_beauty_product = Product.objects.filter(categories__name='BEAUTY', new_arrivals=True, published ='Published').order_by('-created_at')[:25]
    else:
        latest_beauty_product = Product.objects.filter(categories__name='BEAUTY', published ='Published').order_by('-created_at')[:25]

    latest_fashion_product = Product.objects.filter(categories__name='CLOTHING', published ='Published').order_by('-created_at')[:25]
    print(latest_fashion_product)
    
    
    # selfcare_kit = ComboProduct.objects.filter(active=True).select_related('product').prefetch_related('product__productimage_set')
    
    selfcare_kit = ComboProduct.objects.filter(active=True).select_related('product')[:25]


    beauty_bestseller = Product.objects.filter(categories__name='BEAUTY', published ='Published', best_seller=True).order_by('-created_at')[:25]
    fashion_bestseller = Product.objects.filter(categories__name='CLOTHING', published ='Published', best_seller=True).order_by('-created_at')[:25]

    deal = Product.objects.filter(Q(categories__name='SALE') & Q(published='Published') & (Q(subcategories__name='50%') | Q(subcategories__name='60%'))).order_by('-created_at')[:25]
    print(deal)

    brands = Brand.objects.all()

    ratings = Rating.objects.select_related('user').order_by('user__username')

    context = {
        'trending_banner':trending_banner,
        'main_banner':main_banner,
        'price_banner':price_banner,
        'foot_banner':foot_banner,
        'skin_routine':skin_routine,
        'latest_beauty_product':latest_beauty_product,
        'latest_fashion_product':latest_fashion_product,
        'beauty_bestseller':beauty_bestseller,
        'fashion_bestseller':fashion_bestseller,
        'selfcare_kit':selfcare_kit,
        'deal':deal,
        'brands':brands,
        'rating':ratings,
    }

    return render(request, 'home.html', context)


def dashboard(request):
    return render(request, 'my_account/dashboard.html')

def user_order(request):
    return render(request, 'my_account/userorder.html')

def userorder_view(request, id):
    return render(request, 'my_account/user_orderview.html')

def gift_card_balance(request):
    return render(request, 'my_account/giftcard.html')

def address(request):
    user = request.user
    billing_address = Address.objects.get(user=user, address_type='Billing')
    shipping_address = Address.objects.get(user=user, address_type='Shipping')
    context = {
        'billing_address':billing_address,
        'shipping_address':shipping_address,
    }
    return render(request, 'my_account/address.html', context)

def billing_update(request):
    user = request.user
    
    try:
        billing_address = Address.objects.get(user=user, address_type='Billing')
    except Address.DoesNotExist:
        billing_address = None

    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address_type = 'Billing'
        print('first_name', first_name)

        if billing_address:
            # Update the existing address
            billing_address.first_name = first_name
            billing_address.last_name = last_name
            billing_address.address_1 = address_1
            billing_address.address_2 = address_2
            billing_address.city = city
            billing_address.postcode = postcode
            # billing_address.country_region = country_region
            # billing_address.state_country = state_country
            billing_address.email = email
            billing_address.phone = phone
        else:
            # Create a new address
            billing_address = Address(
                user=user,
                first_name=first_name,
                last_name=last_name,
                address_1=address_1,
                address_2=address_2,
                city=city,
                postcode=postcode,
                # country_region=country_region,
                # state_country=state_country,
                email=email,
                phone=phone,
                address_type=address_type
            )
        billing_address.save()
        return redirect('address')  # Redirect to a success URL
    

    context = {
        'billing_address': billing_address,
    }
    return render(request, 'my_account/billingupdate.html', context)

def shipping_update(request):
    user = request.user
    
    try:
        shipping_address = Address.objects.get(user=user, address_type='Shipping')
    except Address.DoesNotExist:
        shipping_address = None


    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address_type = 'Shipping'
        print('first_name', first_name)

        if shipping_address:
            # Update the existing address
            shipping_address.first_name = first_name
            shipping_address.last_name = last_name
            shipping_address.address_1 = address_1
            shipping_address.address_2 = address_2
            shipping_address.city = city
            shipping_address.postcode = postcode
            # shipping_address.country_region = country_region
            # shipping_address.state_country = state_country
            shipping_address.email = email
            shipping_address.phone = phone
        else:
            # Create a new address
            shipping_address = Address(
                user=user,
                first_name=first_name,
                last_name=last_name,
                address_1=address_1,
                address_2=address_2,
                city=city,
                postcode=postcode,
                # country_region=country_region,
                # state_country=state_country,
                email=email,
                phone=phone,
                address_type=address_type
            )
        shipping_address.save()
        return redirect('address')  # Redirect to a success URL


    context = {
        'shipping_address': shipping_address,
    }
    return render(request, 'my_account/shippingupdate.html', context)

def warranty_requests(request):
    return render(request, 'my_account/warrantyrequest.html')

def edit_account(request):
    return render(request, 'edit_account.html')

def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            reset_link = request.build_absolute_uri(reverse('reset_password'))
            
            # Render email template
            email_subject = 'Password Reset Request'
            email_body = render_to_string('email/password_reset.html', {'user': user, 'reset_link': reset_link})
            
            # Send email
            email_message = EmailMessage(subject=email_subject, body=email_body, to=[email])
            email_message.content_subtype = 'html'  # Specify the content subtype as HTML
            email_message.send()
            # Store the OTP and its creation time in the session
            request.session['email'] = email # Store the email in the session
            print(request.session['email'] )
            return JsonResponse({'message': 'Password reset email sent!'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Email not found!'}, status=404)
    return render(request, 'base/forgot_password.html')


# Reset Password Function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    print("reset_password page")
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'base/reset_password.html', {'error': 'Passwords do not match'})
        email = request.session.get('email')
        user = get_user_model().objects.get(email=email)
        print(user)
        request.session['user_id'] = user.id
        user = get_user_model().objects.get(id=request.session.get('user_id'))
        user.set_password(password)
        user.save()
        print("password update")
        del request.session['user_id']
        return redirect('signup')
    breadcrumbs = [
        {'text': 'Home', 'url': '/'},  
        {'text': 'Myaccount', 'url': f'/profile'},
        {'text': 'Forgot Password', 'url': f'/forgot_password'}, 
        {'text': 'Verify OTP'    , 'url': f'/verify_otp'},  
        {'text': 'Reset Password', 'url': f'/reset_password'},  
    ]
    context = {
        'breadcrumbs':breadcrumbs,
    }
    return render(request, 'base/reset_password.html', context)