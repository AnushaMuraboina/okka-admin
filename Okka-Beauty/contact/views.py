from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *
from .forms import ContactForm
import json
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
@csrf_exempt
def contact(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = ContactForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Signup successful'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    contacts = Contact_details.objects.all()
    context = {'contacts': contacts}
    return render(request, 'Contact/contact.html', context)