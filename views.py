from django.shortcuts import render, redirect, get_object_or_404

import os

import xlwt
import xlrd
from django.http import HttpResponseRedirect
import openpyxl
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from Alsuwaidi_Admin.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  
from product.models import *
from checkout.models import *
from user.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from django.views.decorators.cache import never_cache, cache_control
import datetime
from datetime import datetime, timedelta
from datetime import date


from django.db.models import Count, Sum , Max, Case, When, F, Value, IntegerField
from django.db.models.functions import TruncMonth, TruncDate

from cart.models import *
# from ratings.models import *

from django.contrib.auth import get_user_model


from django_filters.views import FilterView
from product.models import Product
from .filters import *

from django.views.generic import ListView
from django.http import HttpResponseServerError


from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from Alsuwaidi_Admin.forms import *


# Category admin  Create, UPdate & Search function

@login_required
def category_admin(request, category_id=None):
    if category_id:
        # Fetch the category instance if the category_id is provided
        category_instance = get_object_or_404(ParentCategory, pk=category_id)
    else:
        category_instance = None

    if request.method == 'POST':
        if category_instance:
            # If category_instance exists, update it
            form = CategoryForm(data=request.POST, files=request.FILES, instance=category_instance)
        else:
            # If not, create a new instance
            form = CategoryForm(data=request.POST, files=request.FILES)
        print('form', form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('category-admin'))
    else:
        # If it's a GET request, populate the form with existing instance data if available
        form = CategoryForm(instance=category_instance)

    category_value = ParentCategory.objects.all()
    
    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Apply search
    if search_query:
        category_value = category_value.filter(name__icontains=search_query)

    user_has_permission = request.user.has_perm('products.view_category')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_category').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'category_value': category_value,
        'form': form,
        'search_query': search_query,
    }
    return render(request, "Al-admin/product/category-admin.html", context)



# Category Delete Function

@login_required
def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = ParentCategory.objects.get(id=category_id)
            print(category)
            category.delete()
            return JsonResponse({'message': 'category deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)



# Sub Category Add, Update, Delete And Search Function

@login_required
def subcategory_admin(request, subcategory_id=None):
    if subcategory_id:
        # Fetch the subcategory instance if the subcategory_id is provided
        subcategory_instance = get_object_or_404(SubCategory, pk=subcategory_id)
    else:
        subcategory_instance = None

    if request.method == 'POST':
        if subcategory_instance:
            # If subcategory_instance exists, update it
            form = SubCategoryForm(request.POST, request.FILES, instance=subcategory_instance)
        else:
            # If not, create a new instance
            form = SubCategoryForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subcategory-admin'))
        
        else:
            print('form not valid ')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # If it's a GET request, populate the form with existing instance data if available
        form = SubCategoryForm(instance=subcategory_instance)

    subCategory_value = SubCategory.objects.all()
    Categorys = ParentCategory.objects.all()
    
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        subCategory_value = subCategory_value.filter(Q(name__icontains=search_query) | 
                                                     Q(description__icontains=search_query))
    if category_filter:
        subCategory_value = subCategory_value.filter(parent_category__name=category_filter)

    user_has_permission = request.user.has_perm('products.view_subcategory')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_subcategory').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')

    context = {
        'subCategory_value': subCategory_value,
        'Categorys': Categorys,
        'form': form,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, "Al-admin/product/subcategory-admin.html", context)

# Sub Category Delete Function

@login_required
def delete_subcategory(request, subcategory_id):
    if request.method == 'POST':
        try:
            Sub_category = SubCategory.objects.get(id=subcategory_id)
            print(Sub_category)
            Sub_category.delete()
            return JsonResponse({'message': 'Subcategory deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Subcategory not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)



# Child Sub category ADD UPDATE DELETE & SEARCH Function

@login_required
def childsubcategory_admin(request, childsubcategory_id=None):
    if childsubcategory_id:
        # Fetch the subcategory instance if the subcategory_id is provided
        childsubcategory_instance = get_object_or_404(ChildSubCategory, pk=childsubcategory_id)
    else:
        childsubcategory_instance = None

    if request.method == 'POST':
        if childsubcategory_instance:
            # If subcategory_instance exists, update it
            form = ChildSubCategoryForm(request.POST, request.FILES, instance=childsubcategory_instance)
        else:
            # If not, create a new instance
            form = ChildSubCategoryForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('childsubcategory-admin'))
        
        else:
            print('form not valid ')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # If it's a GET request, populate the form with existing instance data if available
        form = ChildSubCategoryForm(instance=childsubcategory_instance)

    subCategory = SubCategory.objects.all()
    Categorys = ParentCategory.objects.all()
    childsubcategory_value = ChildSubCategory.objects.all()
    
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        childsubcategory_value = childsubcategory_value.filter(Q(name__icontains=search_query) | 
                                                     Q(description__icontains=search_query))
    if category_filter:
        childsubcategory_value = childsubcategory_value.filter(sub_category__name=category_filter)

    user_has_permission = request.user.has_perm('products.view_subcategory')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_subcategory').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')

    context = {
        'subCategory': subCategory,
        'Categorys': Categorys,
        'form': form,
        'selected_category': category_filter,
        'search_query': search_query,
        'childsubcategory_value':childsubcategory_value,
    }
    return render(request, "Al-admin/product/childsubcategory-admin.html", context)



# Childe Sub Category Delete function

@login_required
def delete_childsubcategory(request, childsubcategory_id):
    if request.method == 'POST':
        try:
            childsubcategory = ChildSubCategory.objects.get(id=childsubcategory_id)
            print(childsubcategory)
            childsubcategory.delete()
            return JsonResponse({'message': 'category deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    


# Brand ADD, UPDATE, DELETE & SEARCH Function

@login_required
def brand_admin(request, brand_id=None):
    if brand_id:
        # Fetch the category instance if the category_id is provided
        brand_instance = get_object_or_404(Brand, pk=brand_id)
    else:
        brand_instance = None
    if request.method == 'POST':
        if  brand_instance:
           # If a POST request is made with brand_id, update the existing record
           form = BrandForm(request.POST, request.FILES, instance=brand_instance)
        else:
           # Otherwise create a new record
            form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('brand-admin'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BrandForm(instance=brand_instance)

    # Retrieve brand values
    brand_value = Brand.objects.all()

    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Apply search
    if search_query:
        brand_value = brand_value.filter(Q(name__icontains=search_query))

    Categorys = ParentCategory.objects.all()

    user_has_permission = request.user.has_perm('products.view_brand')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_brand').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'brand_value': brand_value,
        'form': form,
        'Categorys': Categorys,
        'search_query': search_query,
    }
    return render(request, "Al-admin/product/brand-admin.html", context)


# Brand Delete Function

@login_required
def delete_brand(request, brand_id):
    if request.method == 'POST':
        try:
            brand = Brand.objects.get(id=brand_id)
            print(brand)
            brand.delete()
            return JsonResponse({'message': 'Brand deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'brand not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)



# Product Add & Update Function
def create_product(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = Product()

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        upsell_formset = UpsellProductFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid() and upsell_formset.is_valid():
            print('form is valid')
            product = form.save()
            formset.instance = product
            formset.save()
            upsell_formset.instance = product
            upsell_formset.save()
            # Redirect to success page
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
        upsell_formset = UpsellProductFormSet(instance=product)

    context = {
        'form': form,
        'formset': formset,
        'upsell_formset': upsell_formset,
    }

    return render(request, 'Al-admin/product/add_product.html', context)

# Product Delete Function

@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            print(product)
            product.delete()
            return JsonResponse({'message': 'product deleted successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)


