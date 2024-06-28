from django.shortcuts import render
from .models import *
from rating.models import *
from django.shortcuts import render, get_object_or_404


# Create your views here.
def privacy_policy(request):
    return render(request, 'cmspage/privacy-policy.html')

def cookie_policy(request):
    return render(request, 'cmspage/cookie-policy.html')


def refund_policy(request):
    return render(request, 'cmspage/refund-policy.html')


def shipping_policy(request):
    return render(request, 'cmspage/shipping-policy.html')

def terms_conditions(request):
    return render(request, 'cmspage/terms-conditions.html')

def disclaimer(request):
    return render(request, 'cmspage/disclaimer.html')

def journal(request):
    ratings = Rating.objects.select_related('user').order_by('user__username')
    context = {
        'rating':ratings,
    }
    return render(request, 'cmspage/journal.html', context)

def magazine_blog(request):
   magazine_cards = MagazineBlog.objects.all()
   return render(request, 'cmspage/magazines_blog.html', {'magazine_cards': magazine_cards})