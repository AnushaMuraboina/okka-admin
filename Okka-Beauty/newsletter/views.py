from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Newsletter
from .forms import NewsletterForm
import json
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
@csrf_exempt
def newsletter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = NewsletterForm(data)
        if form.is_valid():
            newsletter = form.save()
            
            # Render the email template with context
            context = {'name': newsletter.name}
            html_content = render_to_string('email/newsletter.html', context)
            
            # Send the email
            subject = 'Thank you for signing up for our newsletter'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [newsletter.email]
            
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return JsonResponse({'status': 'success', 'message': 'Signup successful'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})