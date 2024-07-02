from django.utils import timezone
from django.conf import settings

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            request.user.last_seen = timezone.now()
            print(request.user.last_seen )
            request.user.save(update_fields=['last_seen'])
            
        return response
