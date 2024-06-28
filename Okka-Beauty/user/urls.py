from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('', views.home, name="home"),
   path('signup/', views.register_view, name='signup'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.sign_out, name ="logout"),
   path('my-account/', views.dashboard, name='my-account'),
   path('my-account/orders/', views.user_order, name='user-order'),
   path('my-account/view-order/<int:id>/', views.userorder_view, name='userorder_view'),
   path('balance/', views.gift_card_balance, name="balance"),
   path('my-account/edit-address/', views.address, name='address'),
   path('my-account/edit-address/billing/', views.billing_update, name='billing_update'),
   path('my-account/edit-address/shipping/', views.shipping_update, name='shipping_update'),
   path('my-account/warranty-requests/', views.warranty_requests, name='warranty_requests'),
   path('my-account/edit-account/', views.edit_account, name='edit_account'),
   path('my-account/forgot-password/', views.forgot_password, name='forgot_password'),
   path('my-account/reset-password/', views.reset_password, name='reset_password'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)