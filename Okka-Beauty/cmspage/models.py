from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User 

# Create your models here.
class MagazineCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class MagazineTags(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class MagazineBlog(models.Model):
    heading = models.CharField(max_length=255 ,default=True)
    feature_image = models.ImageField(upload_to='media')
    category = models.ForeignKey(MagazineCategory, on_delete=models.CASCADE)
    tag = models.ForeignKey(MagazineTags, on_delete=models.CASCADE)
    description = RichTextField()
    publish_date = models.DateField()  


    def __str__(self):
        return self.header
    

    @property
    def display_date(self):
        # Return only the date part of publish_date
        return self.publish_date.strftime('%d')

    @property
    def display_month(self):
        # Return the month part of publish_date as text
        return self.publish_date.strftime('%B')

    def save(self, *args, **kwargs):
       user = kwargs.pop('user', None)
       if user and isinstance(user, User):
          self.author = user
       super().save(*args, **kwargs)