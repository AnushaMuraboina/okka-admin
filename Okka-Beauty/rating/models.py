from django.db import models
from user.models import *
from product.models import *
from django.utils.html import mark_safe


# Create your models here.
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField()
    review = models.TextField()
    anonymous = models.BooleanField(default=False)
    review_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def display_stars(self):
        full_stars = int(self.stars)
        half_star = self.stars - full_stars
        empty_stars = 5 - full_stars - (1 if half_star else 0)

        full_star_icon = '<i class="fas fa-star"></i>'
        half_star_icon = '<i class="fas fa-star-half-alt"></i>'
        empty_star_icon = '<i class="far fa-star"></i>'

        stars_html = (full_star_icon * full_stars +
                      (half_star_icon if half_star else '') +
                      empty_star_icon * empty_stars)

        return mark_safe(stars_html)

    def __str__(self):
        return f"Rating for {self.product.name} by {self.user.username}"

class RatingImage(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='rating_images/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Image for rating by {self.rating.user.username}"