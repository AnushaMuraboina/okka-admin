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
        subCategory_value = subCategory_value.filter(main_Category__name=category_filter)

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
