from django.db import models
from product.models import *
# Create your models here.
class MainBanner(models.Model):
    # category = models.ForeignKey(ChildSubCategory, on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='media/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.url} Banner - {self.url}"

class TrendingBrand(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_image = models.ImageField(upload_to='trending_brands/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand.name} Trending Brand - {self.url}"
    

class PriceBanner(models.Model):
    # Category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='media/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Category.name} Trending Brand - {self.image}"
    

class FooterBanner(models.Model):
    # category = models.ForeignKey(ChildSubCategory, on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='media/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.url} Banner - {self.url}"
    

class WhyUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='why_us/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title
