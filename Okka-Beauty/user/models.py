from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_nicename = models.CharField(max_length=50)
    display_name = models.CharField(max_length=250)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

class OkdUsers(models.Model):
    ID = models.BigAutoField(primary_key=True)
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=255)
    user_nicename = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100)
    user_url = models.URLField(max_length=100)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=255)
    user_status = models.IntegerField(default=0)
    display_name = models.CharField(max_length=250)

    class Meta:
        db_table = 'okd_users'
