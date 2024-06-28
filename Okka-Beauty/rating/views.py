from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import logging
from .models import *

logger = logging.getLogger(__name__)

@csrf_exempt
def submit_rating(request):
    if request.method == 'POST':
        print('rating post function work')
        print(request.POST)
        logger.debug('Received POST request for submit_rating')
        
        user = request.user
        print(user)
        product_id = request.POST.get('product_id')
        print(product_id)
        
        product = get_object_or_404(Product, id=product_id)
        print(product)
        
        stars = request.POST.get('stars')
        print(stars)
        
        review = request.POST.get('review')
        print(review)
        
        anonymous = request.POST.get('anonymous', False)

        rating = Rating.objects.create(
            user=user,
            product=product,
            stars=stars,
            review=review,
            anonymous=anonymous,
        )

        for image in request.FILES.getlist('images'):
            RatingImage.objects.create(rating=rating, photo=image)

        return JsonResponse({'message': 'Rating submitted successfully!'}, status=201)
    else:
        logger.debug('Received non-POST request for submit_rating')
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

