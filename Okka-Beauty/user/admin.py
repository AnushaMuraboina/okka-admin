from django.contrib import admin
from .models import *
# Register your models here.

class OkdUsersAdmin(admin.ModelAdmin):
    list_display = ('user_login', 'user_email', 'user_registered', 'user_status')  # Customize this list as needed
    search_fields = ('user_login',)  # Enable search based on the user_login field

admin.site.register(OkdUsers, OkdUsersAdmin)

admin.site.register(User)