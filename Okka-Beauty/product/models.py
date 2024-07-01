from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class ParentCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='parent_category_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keyword = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    include_in_navigation_menu = models.BooleanField(default=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keyword = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    include_in_navigation_menu = models.BooleanField(default=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    skin_routine = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ChildSubCategory(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='child_sub_category_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keyword = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    include_in_navigation_menu = models.BooleanField(default=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='brand_images/', null=True, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    TYPE_CHOICES = [
        ('simple', 'simple'),
        ('variation', 'variation'),
        ('variable', 'variable'),
        ('Grouped', 'Grouped'),
        ('External', 'External'),
        # Add more types as needed
    ]

    IN_STOCK_CHOICES = [
        ('Instock', 'Instock'),
        ('Outofstock', 'Outofstock'),
    ]
    STATUS =[
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Private', 'Private'),

    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # sku = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    # published = models.BooleanField(default=False)
    published = models.CharField(max_length=20, choices=STATUS)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    in_stock = models.CharField(max_length=10, choices=IN_STOCK_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    low_stock_amount = models.PositiveIntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    # categories = models.ForeignKey('ParentCategory', on_delete=models.CASCADE)
    # subcategories = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    # childsubsategories = models.ForeignKey('ChildSubCategory', on_delete=models.CASCADE)
    # brands = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField(ParentCategory, blank=True)
    subcategories = models.ManyToManyField(SubCategory, blank=True)
    childsubcategories = models.ManyToManyField(ChildSubCategory, blank=True)
    brands = models.ManyToManyField(Brand, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    allow_customer_reviews = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag')
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_keyword = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    new_arrivals = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

def product_image_upload_path(instance, filename):
    # Get the current year and month
    year = timezone.now().year
    month = timezone.now().month
    # Build the upload path
    upload_to = 'product_images/{0}/{1}/{2}'.format(year, month, filename)
    return upload_to

class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    slot_position = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.image.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already set
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Attribute(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    slot_position = models.IntegerField()

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    slot_position = models.IntegerField()

    def __str__(self):
        return self.value
    


class UpsellProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    upsell_products = models.ManyToManyField('Product', related_name='upsell_products')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Upsell Products for {self.product.name}"

class CrossSellProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    cross_sell_products = models.ManyToManyField('Product', related_name='cross_sell_products')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cross Sell Products for {self.product.name}"
    

class ComboProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    Combo_products = models.ManyToManyField('Product', related_name='ComboProduct')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Combo Products for {self.product.name}"