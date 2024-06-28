import django_filters
from product.models import Product
from django.db.models import Q
from django import forms
# from csvdata.models import *
# class ProductFilter(django_filters.FilterSet):
    
#     class Meta:
#         model = products
#         fields = {
#             # 'product_name': ['icontains'],
#             # 'model_number': ['icontains'],
#             # 'product_sku': ['exact'],
#             'brand': ['exact'],
#             'category': ['exact'],
#             'sub_category': ['exact'],
#             # 'price': ['exact', 'gte', 'lte'],
#             'stock_status': ['exact'],
#             # Add other fields as needed
#         }
#         widgets = {
#             'brand': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
#             'category': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
#             'sub_category': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
#             'stock_status': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
#             # Add other fields as needed
#         }

#     @property
#     def form(self):
#         form = super().form
#         for field_name, field in form.fields.items():
#             # Add custom class to each form field
#             field.widget.attrs['class'] = 'form-select filter-dropdown'
#         return form

class CustomSearchInput(forms.widgets.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control search-input search', 'type': 'search', 'placeholder': 'Search products', 'aria-label': 'Search'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=CustomSearchInput()  # Use your custom widget here
    )

    class Meta:
        model = Product
        fields = {
            'brands': ['exact'],
            'categories': ['exact'],
            'subcategories': ['exact'],
            # 'stock_status': ['exact'],
            # Add other fields as needed
        }
        widgets = {
            'brand': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            'categories': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            'subcategories': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # 'stock_status': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # Add other fields as needed
        }

    @property
    def form(self):
        form = super().form
        for field_name, field in form.fields.items():
            # Add custom class to each form field
            field.widget.attrs['class'] = 'form-select filter-dropdown'
        return form

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(product_name__icontains=value) |
            # Q(model_number__icontains=value) |
            Q(product_sku__exact=value)
            # Add other fields as needed
        )
    


class csv_CreationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=CustomSearchInput()  # Use your custom widget here
    )
    class Meta:
        # model = csv_Creation
        fields = {
            'badge_no': ['exact'],
        }

        widgets = {
            'badge_no': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # 'category': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # 'sub_category': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # 'stock_status': django_filters.widgets.LinkWidget(attrs={'class': 'form-select filter-dropdown'}),
            # Add other fields as needed
        }

    @property
    def form(self):
        form = super().form
        for field_name, field in form.fields.items():
            # Add custom class to each form field
            field.widget.attrs['class'] = 'form-select filter-dropdown'
        return form
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(product_name__icontains=value) |
            # Q(model_number__icontains=value) |
            Q(brands_name__icontains=value) |
            Q(categories_name__icontains=value) |
            Q(subcategories_name__icontains=value) |
            Q(description__icontains=value) |
            Q(short_description__icontains=value) |
            # Q(warranty_conditions__icontains=value) |
            Q(stock__icontains=value) 
            # Q(item_no__icontains=value)
            # Add other fields as needed
        )