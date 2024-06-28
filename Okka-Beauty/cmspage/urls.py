from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
   path('cookie-policy/', views.cookie_policy, name='cookie-policy'),
   path('refund-policy/', views.refund_policy, name='refund-policy'),
   path('shipping-policy/', views.shipping_policy, name='shipping-policy'),
   path('terms-and-conditions/', views.terms_conditions, name='terms-and-conditions'),
   path('disclaimer/', views.disclaimer, name='disclaimer'),
   path('reviews/', views.journal, name='disclaimer'),
   path('blog/', views.magazine_blog, name="blog"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)