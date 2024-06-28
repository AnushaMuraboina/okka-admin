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

# Create your views here.

@login_required
def custom_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            # Redirect to a success page or do whatever you want
            return redirect('customer')  # Replace 'success_page' with the name of your success page URL
        else:
            print('form not valid ')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'Al-admin/customer/new_customer.html', {'form': form})


User = get_user_model()

def export_user_data_as_csv(request):
    users = User.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_data.csv"'

    # fieldnames = ['Email', 'First Name', 'Last Name', 'Gender', 'Date of Birth', 'Phone', 'Alternative Phone', 'Address']
    fieldnames = [' ID ','Email', ' user_nicename', 'display_name ', 'user_status ', 'user_activation_key', 'user_pass', ' user_url ']

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()

    for user in users:
        try:
            user_profile = OkdUsers.objects.get(user=user)
            writer.writerow({
                ' ID ':user_profile.ID ,
                'Email': user.email,
                'First Name': user_profile.user_nicename,
                'display_name ': user_profile.display_name ,
                'user_status ': user_profile.user_status ,
                'user_activation_key': user_profile.user_activation_key,
                'user_pass': user_profile.user_pass,
                ' user_url ': user_profile.user_url ,
                # 'Address': user_profile.address,
            })
        except OkdUsers.DoesNotExist:
            writer.writerow({
                'Email': user.email,
                'First Name': '',
                'display_name ': '',
                'user_status ': '',
                'Date of Birth': '',
                'user_pass': '',
                ' user_url ': '',
                # 'Address': '',
            })

    return response




@login_required
@csrf_exempt 
def product_adding(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        # print(data)
        print(request.POST)
        product_name = request.POST.get('name')
        print(product_name)
        product_description = request.POST.get('description')
        print(product_description)
        short_description = request.POST.get('short_description')  
        print(short_description)
        type = request.POST.get('type')
        print(type)
        published = request.POST.get('published ')
        print(published )
        in_stock= request.POST.get('in_stock')
        print(in_stock)
        sku = request.POST.get('sku')
        print(sku)
        category = request.POST.get('categories ')
        print(category)
        subcategory = request.POST.get('subcategories')
        print(subcategory)
        childsubcategories= request.POST.get('childsubcategories')
        print(childsubcategories )
        brand = request.POST.get('brands')
        print(brand)
        stock = request.POST.get('stock ')
        print(stock )
        low_stock_amount= request.POST.get('low_stock_amount')
        print(low_stock_amount)
        sale_price  = request.POST.get(' sale_price ')
        print( sale_price )
        regular_price= request.POST.get(' regular_price')
        print(regular_price )
        weight  = request.POST.get('weight  ')
        print(weight  )
        length= request.POST.get('length ')
        print( length)
        width= request.POST.get('width ')
        print(width )
        height= request.POST.get(' height')
        print(height )
        allow_customer_reviews = request.POST.get(' allow_customer_reviews')
        print(allow_customer_reviews )
        tags  = request.POST.get('tags  ')
        print(tags )
        seo_title = request.POST.get('seo_title')
        print(seo_title )
        seo_keyword  = request.POST.get(' seo_keyword ')
        print(seo_keyword  )
        seo_description = request.POST.get('seo_description ')
        print(seo_description )
        new_arrivals   = request.POST.get('new_arrivals   ')
        print(new_arrivals  )
        best_seller= request.POST.get('best_seller  ')
        print(best_seller  )
        created_at  = request.POST.get(' created_at  ')
        print(created_at  )

        attribute = request.POST.getlist('attribute')
        print(attribute)
        attributeValue = request.POST.getlist('attributeValue')
        print(attributeValue)
        upsell_product = request.POST.get('upsell_product')
        print('upsell products')
        print( upsell_product)

        product_images = request.FILES.getlist('images[]')
        # product_images = product_images_string.split(',')
        # print(product_images)

        # Find the corresponding Brand instance based on the provided brand name
        try:
            brand_instance = Brand.objects.get(name=brand)
            print('Brand Instance Value',brand_instance)
        except Brand.DoesNotExist:
            return JsonResponse({'message': 'Brand does not exist'})
        

        # Find the corresponding category instance based on the provided category name
        try:
            category_instance = ParentCategory.objects.get(name=category)
            print('Category Instance Value', category_instance)
        except ParentCategory.DoesNotExist:
            return JsonResponse({'message': 'category does not exist'})
        
        # Find the corresponding category instance based on the provided category name
        try:
            sub_category_instance = SubCategory.objects.get(name=subcategory)
            print('Sub Category Instance Value',sub_category_instance)
        except SubCategory.DoesNotExist:
            return JsonResponse({'message': 'subCategory does not exist'})

        # Check if a product with the same SKU already exists
        existing_product = Product.objects.filter(product_sku=sku).first()
        print('existing_product Value', existing_product)

        if existing_product:
            return JsonResponse({'message': 'Product already exist'})

        else:
            product = Product(
                product_name=product_name,
                product_sku = sku, 
                brand = brand_instance, 
                category = category_instance, 
                sub_category = sub_category_instance, 
                description = product_description, 
                short_description = short_description, 
                # warranty_conditions = Warranty, 
                # price = price, 
                regular_price=regular_price,
                sale_price =sale_price ,
                # special_price = special_price, 
                weight = weight, 
                stock = stock, 
                # in_stock = in_stock,
                # product_Image1=product_images[0] if len(product_images) > 0 else None,
                # product_Image2=product_images[1] if len(product_images) > 1 else None,
                # product_Image3=product_images[2] if len(product_images) > 2 else None,
                # product_Image4=product_images[3] if len(product_images) > 3 else None,
                
            )

            if sale_price:
                product.sale_price = sale_price

            # Conditionally assign weight if not empty
            if weight:
                product.weight = weight

            # Conditionally assign warranty_conditions if not empty
            # if Warranty:
            #     product.warranty_conditions = Warranty

            # for i in range(4):  # Assuming you have 4 image fields as per your model
            #     if i < len(product_images):
            #         setattr(product, f'product_Image{i+1}', os.path.join('product', product_images[i].strip('/')))


            # Define the directory where you want to save the uploaded images
            # UPLOAD_DIR = 'product/'  # Relative path within MEDIA_ROOT
            UPLOAD_DIR = 'media/'  # Relative path within MEDIA_ROOT
            absolute_upload_dir = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR)
            
            # Create the upload directory if it doesn't exist
            if not os.path.exists(absolute_upload_dir):
                os.makedirs(absolute_upload_dir)
            
            for image_path in product_images: 
                # Create a new filename to avoid clashes and potential security issues
                new_filename = os.path.join(absolute_upload_dir, image_path.name)
                
                # Save the uploaded image to the specified directory
                with open(new_filename, 'wb') as f:
                    f.write(image_path.read())
                        
                product_image_instance = ProductImage.objects.create(
                    product=product,
                    image=os.path.join(UPLOAD_DIR, image_path.name),
                )

            product.save()
            print(product)

            if upsell_product:
                # Store upsell products in the ProductUpsell model
                for upsell_sku in upsell_product.split(','):
                    try:
                        upsell_product_instance = Product.objects.get(id=upsell_sku)
                        # product_upsell = ProductUpsell(product=product, upsell_product=upsell_product_instance)
                        product_upsell = UpsellProduct(product=product, upsell_products=upsell_product_instance)
                        product_upsell.save()
                        print('Upsell product stored successfully')
                    except Product.DoesNotExist:
                        print(f'Upsell product with SKU {upsell_sku} does not exist')


        product_instance = Product.objects.get(pk=product.id)  # Replace with the appropriate way to get the product instance
        print(product_instance)
        subcategory_instance = SubCategory.objects.get(name=product.sub_category)  # Replace with the appropriate way to get the subcategory instance
        print(subcategory_instance)
        # for attribute_name, attribute_value_name in zip(attribute, attributeValue):
        # for attribute_value_name in attributeValue:
        for attribute_value_name in attributeValue:
            try:
                attribute_value_instance = AttributeValue.objects.get(value=attribute_value_name)
                
                # product_attr_values_instance = product_attr_values_map(               #MAIN
                #     product=product_instance,
                #     subcategory=subcategory_instance,
                #     attribute=attribute_value_instance.attribute,
                #     attribute_value=attribute_value_instance,  # Assign the instance, not the name
                #     active=True
                # )
                # product_attr_values_instance.save()
                            
            except ObjectDoesNotExist:
                # Handle cases where the hierarchy is not maintained
                print("Invalid hierarchical relationship detected")
                # You might want to handle this based on your application's requirements


            
        return JsonResponse({'message': 'Product added successfully'})
    
    products_list = Product.objects.all()
    # Number of items to display per page
    items_per_page = 30

    # Create a Paginator object
    paginator = Paginator(products_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the products for the current page
        products_page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, deliver the last page of results.
        products_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products_page = paginator.page(1)
    
    Categorys = ParentCategory.objects.all()
    subCategories = SubCategory.objects.all()
    brand = Brand.objects.all()
    attribute = Attribute.objects.all()
    form3 = CategoryForm()
    form1 = SubCategoryForm()
    form2 = BrandForm()
    comtext = {
        'product': products_page,
        'Categorys':Categorys,
        'subCategories':subCategories,
        'brand':brand,
        'attribute':attribute,
        # 'form3':form3,
        # 'form1':form1,
        # 'form2':form2,
    }
    
    return render(request, "Al-admin/product/product_adding.html", comtext)

# Upsell function

# def upsell_selection(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         selected_values = data.get('selectedValues')
#         print(selected_values)

#         upsell_product = [product for product in products.objects.filter(id__in=selected_values)]
#         print(upsell_product)
        
#         serialized_data = serializers.serialize('json', upsell_product)

#         return JsonResponse(serialized_data, safe=False)


@login_required
def upsell_selection(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_values = data.get('selectedValues')
        print(selected_values)
        
        upsell_product = Product.objects.values('pk','name', 'sku', 'image', 'category__name', 'sub_category__name', 'brand__name', 'stock','in_stock', 'regular_price',' sale_price', 'active').filter(id__in=selected_values)
        product_data = list(upsell_product)
        print(product_data)
        
        return JsonResponse(product_data, safe=False)



# def product_admin(request):

#     products_list = products.objects.all()
#     all_count = products_list.count()
#     publish_count = products.objects.filter(active = True).count()
#     unpublish_count = products.objects.filter(active = False).count()
#     outofstock_count = products.objects.filter(in_stock = 'Out of Stock').count()
#     categories = Category.objects.all()
#     subCategories = subCategory.objects.all()
#     brand = Brand.objects.all()

#     # Number of items to display per page
#     items_per_page = 30

#     # Create a Paginator object
#     paginator = Paginator(products_list, items_per_page)

#     # Get the current page number from the request
#     page_number = request.GET.get('page')

#     try:
#         # Get the products for the current page
#         products_page = paginator.page(page_number)
#     except EmptyPage:
#         # If the requested page is out of range, deliver the last page of results.
#         products_page = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         # If the page parameter is not an integer, deliver the first page.
#         products_page = paginator.page(1)

#     context = {
#         'product': products_page,
#         'categories': categories,
#         'subCategories': subCategories,
#         'brand': brand,
#         'all_count':all_count,
#         'publish_count':publish_count,
#         'unpublish_count':unpublish_count,
#         'outofstock_count':outofstock_count,
#     }
    
#     return render(request, "Al-admin/product/product_admin.html", context)


@login_required
def product_update(request, product_id):

    product_data = Product.objects.get(id=product_id)

    product_images = product_data.images.all()

    upsell_product = UpsellProduct.objects.filter(product=product_data).values('upsell_product__pk','upsell_product__product_name', 'upsell_product__product_sku', 'upsell_product__model_number', 'upsell_product__image ', 'upsell_product__category__name', 'upsell_product__sub_category__name', 'upsell_product__brand__name', 'upsell_product__stock', 'upsell_product__number_of_stock_out', 'upsell_product__price','regular_price' , 'upsell_product__active')
    # product_data = list(upsell_product)
    print('Upsell Product',upsell_product)

    if request.method == 'POST':
        # data = json.loads(request.body)
        # print(data)
        print('Update product axios post a value')
        print(request.POST)

        product_name = request.POST.get('name')
        print(product_name)
        product_description = request.POST.get('description')
        print(product_description)
        short_description = request.POST.get('short_description')  
        print(short_description)
        type = request.POST.get('type')
        print(type)
        published = request.POST.get('published ')
        print(published )
        in_stock= request.POST.get('in_stock')
        print(in_stock)
        sku = request.POST.get('sku')
        print(sku)
        category = request.POST.get('categories ')
        print(category)
        subcategory = request.POST.get('subcategories')
        print(subcategory)
        childsubcategories= request.POST.get(' childsubcategories')
        print(childsubcategories )
        brand = request.POST.get('brands')
        print(brand)
        stock = request.POST.get('stock ')
        print(stock )
        low_stock_amount= request.POST.get('low_stock_amount')
        print(low_stock_amount)
        sale_price  = request.POST.get(' sale_price ')
        print( sale_price )
        regular_price= request.POST.get(' regular_price')
        print(regular_price )
        weight  = request.POST.get('weight  ')
        print(weight  )
        length= request.POST.get('length ')
        print( length)
        width= request.POST.get('width ')
        print(width )
        height= request.POST.get(' height')
        print(height )
        allow_customer_reviews = request.POST.get(' allow_customer_reviews')
        print(allow_customer_reviews )
        tags  = request.POST.get('tags  ')
        print(tags )
        seo_title = request.POST.get('seo_title')
        print(seo_title )
        seo_keyword  = request.POST.get(' seo_keyword ')
        print(seo_keyword  )
        seo_description = request.POST.get('seo_description ')
        print(seo_description )
        new_arrivals   = request.POST.get('new_arrivals   ')
        print(new_arrivals  )
        best_seller= request.POST.get('best_seller  ')
        print(best_seller  )
        created_at  = request.POST.get(' created_at  ')
        print(created_at  )


        product_images = request.FILES.getlist('images[]')
        print('product_images', product_images)
        product_images_string = request.POST.get('file')
        if product_images_string is not None:
            product_images = product_images_string.split(',')
            print(product_images)

            

        # Find the corresponding Brand instance based on the provided brand name
        try:
            brand_instance = Brand.objects.get(name=brand)
        except Brand.DoesNotExist:
            return JsonResponse({'message': 'Brand does not exist'})
        

        # Find the corresponding category instance based on the provided category name
        try:
            category_instance = ParentCategory.objects.get(name=category)
        except ParentCategory.DoesNotExist:
            return JsonResponse({'message': 'category does not exist'})
        
        # Find the corresponding category instance based on the provided category name
        try:
            sub_category_instance = SubCategory.objects.get(name=subcategory)
        except SubCategory.DoesNotExist:
            return JsonResponse({'message': 'subCategory does not exist'})

        # Check if a product with the same SKU already exists
        existing_product = Product.objects.get(product_sku=sku)

        existing_product.name=product_name
        # existing_product.model_number = model
        existing_product.sku = sku
        existing_product.brands = brand_instance
        existing_product.categories = category_instance
        existing_product.subcategories= sub_category_instance
        existing_product.description = product_description
        existing_product.short_description = short_description 
        existing_product.regular_price= regular_price
        existing_product.stock  = stock
        # existing_product.in_stock = in_stock

        # Conditionally assign special_price if not empty
        if sale_price:
            existing_product.sale_price = sale_price
        # Conditionally assign weight if not empty
        if weight:
            existing_product.weight = weight
        # Conditionally assign warranty_conditions if not empty
        # if Warranty:
        #     existing_product.warranty_conditions = Warranty

        existing_product.save()


        # Define the directory where you want to save the uploaded images
        UPLOAD_DIR = 'media/'  # Relative path within MEDIA_ROOT
        absolute_upload_dir = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR)
            
        # Create the upload directory if it doesn't exist
        if not os.path.exists(absolute_upload_dir):
            os.makedirs(absolute_upload_dir)
            
        for image_path in product_images: 
            # Create a new filename to avoid clashes and potential security issues
            new_filename = os.path.join(absolute_upload_dir, image_path.name)
                
            # Save the uploaded image to the specified directory
            with open(new_filename, 'wb') as f:
                f.write(image_path.read())

            product_image_instance =ProductImage.objects.create(
                    product=existing_product,
                    image=os.path.join(UPLOAD_DIR, image_path.name),
            )


        # for image_path in product_images:
        #     image_path = image_path.strip()  # Remove leading/trailing spaces if necessary

        #     if image_path:
        #         #  Check if the image_path starts with "product/" and add it if it doesn't
        #         if not image_path.startswith('product/'):
        #             image_path = os.path.join('product', image_path.strip('/'))

        #         try:
        #             # Try to retrieve an existing image instance with the same path
        #             existing_image = product_image.objects.filter(product=existing_product, image=image_path)
        #             print(f'Image "{image_path}" already exists for the product. Skipping...')
        #         except ObjectDoesNotExist:
        #             # Create and save the product_image_instance
        #             product_image_instance = product_image.objects.create(
        #                 product=existing_product,
        #                 image=image_path,
        #             )
        #             print(f'Image "{image_path}" uploaded successfully')

        ## Process the product_attr_values_map data
        # for attr, attr_value in zip(attribute,attributeValue):
        #     # Find the corresponding Attribute and AttributeValue instances
        #     try:
        #         attribute_instance = Attribute.objects.get(name=attr)
        #         attribute_value_instance = AttributeValue.objects.get(attribute=attribute_instance, value=attr_value)
        #     except Attribute.DoesNotExist:
        #         return JsonResponse({'message': f'Attribute "{attr}" does not exist'})
        #     except AttributeValue.DoesNotExist:
        #         return JsonResponse({'message': f'AttributeValue "{attr_value}" does not exist'})

            ## Check if a product_attr_values_map with the same values already exists
            # existing_mapping = product_attr_values_map.objects.filter(
            #     product=existing_product,
            #     subcategory=sub_category_instance,
            #     attribute=attribute_instance,
            #     attribute_value=attribute_value_instance,
            # ).first()

            # if existing_mapping:
            #     # Update the existing mapping
            #     existing_mapping.Active = True  # Modify this based on your requirements
            #     existing_mapping.save()
            # else:
    
                # Create a new mapping
                # new_mapping = product_attr_values_map.objects.create(
                #     product=existing_product,
                #     subcategory=sub_category_instance,
                #     attribute=attribute_instance,
                #     attribute_value=attribute_value_instance,
                #     Active=True,  # Modify this based on your requirements
                # )
                # print(f'New product_attr_values_map created: {new_mapping}')

        # upsell_skus = upsell_product.split(',')

        # for upsell_id in upsell_product.split(','):
        #     try:
        #         upsell_product_instance = products.objects.get(id=upsell_id)
        #         # Check if the product is already associated with this upsell product
                # if not ProductUpsell.objects.filter(product=product_id, upsell_product=upsell_product_instance).exists():
                #     product_upsell = ProductUpsell(product=product_id, upsell_product=upsell_product_instance)
                #     product_upsell.save()
                #     print(f'Upsell product with SKU {upsell_id} stored successfully')
                # else:
                #     print(f'Upsell product with SKU {upsell_id} is already associated with the product')
        #     except ObjectDoesNotExist:
        #         print(f'Upsell product with SKU {upsell_id} does not exist')


        if upsell_product:
            # Split the incoming upsell_product string into a list of upsell IDs
            new_upsell_ids = set(upsell_product.split(','))
            new_upsell_ids = set(int(id) for id in new_upsell_ids)
            print('new_upsell_ids', new_upsell_ids)

            # Retrieve the existing upsell products associated with the product
            existing_upsell_products = UpsellProduct.objects.filter(product=product_data)
            print('existing_upsell_products', existing_upsell_products)

            # Create a set of existing upsell IDs
            existing_upsell_ids = set(up.upsell_product.id for up in existing_upsell_products)
            print('existing_upsell_ids', existing_upsell_ids)

            # Find upsell IDs to be deleted (in existing set but not in new set)
            upsell_ids_to_delete = existing_upsell_ids - new_upsell_ids
            print('upsell_ids_to_delete', upsell_ids_to_delete)

            # Find new upsell IDs to be added (in new set but not in existing set)
            upsell_ids_to_add = new_upsell_ids - existing_upsell_ids
            print('upsell_ids_to_add', upsell_ids_to_add)

            upsell_ids_to_delete = [id for id in upsell_ids_to_delete if id not in new_upsell_ids]
            print('upsell_ids_to_delete', upsell_ids_to_delete)

            # Delete the upsell products that are no longer associated with the product
            upsell_delete = UpsellProduct.objects.filter(product=product_data, upsell_product__id__in=upsell_ids_to_delete).delete()
            print(f'upsell product deleted {upsell_delete}')

            # Add new upsell products that are not already associated with the product
            for upsell_id in upsell_ids_to_add:
                try:
                    upsell_product_instance = Product.objects.get(id=upsell_id)
                    if not UpsellProduct.objects.filter(product=product_data, upsell_product=upsell_product_instance).exists():
                        product_upsell = UpsellProduct(product=product_data, upsell_product=upsell_product_instance)
                        product_upsell.save()
                        print(f'Upsell product with SKU {upsell_id} stored successfully')
                    else:
                        print(f'Upsell product with SKU {upsell_id} is already associated with the product')
                except Product.DoesNotExist:
                    print(f'Upsell product with ID {upsell_id} does not exist')

            # Print a message for removed upsell products
            for upsell_ids_to_delete in upsell_ids_to_delete:
                print(f'Upsell product with ID {upsell_ids_to_delete} has been removed')

        else:
            print('Upsell products list is empty.')


        return JsonResponse({'message': 'Product updated successfully'})

    

    Categorys = ParentCategory.objects.all()
    subCategories = SubCategory.objects.all()
    brand = Brand.objects.all()

    # attribute = Category_attribute_map.objects.filter(subCategory = product_data.sub_category)




    products_list = Product.objects.all()
    # Number of items to display per page
    items_per_page = 30

    # Create a Paginator object
    paginator = Paginator(products_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the products for the current page
        products_page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, deliver the last page of results.
        products_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products_page = paginator.page(1)

    comtext = {
        'product_data':product_data,
        'product_images': product_images,
        'Categorys':Categorys,
        'subCategories':subCategories,
        'brand':brand,
        # 'attribute':attribute,
        'product': products_page,
        'product_id':product_id,
        # 'upsell_product':upsell_product,
    }
    return render(request, "Al-admin/product/product_adding.html", comtext)


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

@login_required
def remove_image(request, image_id):
    print(image_id)
    try:
        image = ProductImage.objects.get(pk=image_id)
        image.delete()
        response_data = {'message': f'Image with ID {image_id} removed successfully.'}
    except ProductImage.DoesNotExist:
        response_data = {'message': f'Image with ID {image_id} not found.'}
    except Exception as e:
        response_data = {'message': f'Error occurred: {str(e)}'}

    return JsonResponse(response_data)

@login_required
def filter_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        filter_type = data.get('filter_type')
        print(filter_type)
        filter_value = data.get('filter_value')
        print(filter_value)

        product = Product.objects.all()

        if filter_type == 'category':
            product = product.values('pk','name', 'sku',  'category__name', 'sub_category__name', 'brand__name', 'stock','in_stock',  'regular_price',  'active').filter(category__name=filter_value)
        elif filter_type == 'subcategory':
            product = product.values('pk','name', 'sku', 'category__name', 'sub_category__name', 'brand__name', 'stock','in_stock',  'regular_price',  'active').filter(sub_category__name=filter_value)
        elif filter_type == 'brand':
            product = product.values('pk','name', 'sku', 'category__name', 'sub_category__name', 'brand__name', 'stock','in_stock',  'regular_price', 'active').filter(brand__name=filter_value)
        else:
           product = product.values('pk','name', 'sku', 'category__name', 'sub_category__name', 'brand__name', 'stock','in_stock',  'regular_price',  'active').filter(in_stock=filter_value)
        
        print(product)
        # Convert the QuerySet to a list
        product_data = list(product)
        # serialized_data = serializers.serialize('json', product)
    
        return JsonResponse(product_data, safe=False)

# def category_admin(request):
#     category_value = Category.objects.all()
#     form = CategoryForm()

#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Apply search
#     if search_query:
#         category_value = category_value.filter(name__icontains=search_query)

#     context = {
#         'category_value': category_value,
#         'form': form,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/product/category-admin.html", context)
    

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


# def subcategory_admin(request):
#     subCategory_value = subCategory.objects.all()
#     Categorys = Category.objects.all()
#     form = SubCategoryForm()
#     context = {
#         'subCategory_value':subCategory_value,
#         'Categorys':Categorys,
#         'form':form,
#     }
#     return render(request, "Al-admin/product/subcategory-admin.html", context)


# @login_required
# def subcategory_admin(request):
#     if request.method == 'POST':
#         form = SubCategoryForm(request.POST, request.FILES)
#         print(form)        
#         if form.is_valid():
#             form.save()
#             # return JsonResponse({'message': 'SubCategory created successfully'})
#             return HttpResponseRedirect(reverse('subcategory-admin'))
#         else:
#             # Add error messages to Django messages framework
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form = SubCategoryForm()
        
#     subCategory_value = subCategory.objects.all()
#     Categorys = Category.objects.all()
    
#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')
#     category_filter = request.GET.get('category', '')

#     # Apply search and filter
#     if search_query:
#         subCategory_value = subCategory_value.filter(Q(name__icontains=search_query) | 
#                                                      Q(description__icontains=search_query))
#     if category_filter:
#         subCategory_value = subCategory_value.filter(main_Category__name=category_filter)

#     context = {
#         'subCategory_value': subCategory_value,
#         'Categorys': Categorys,
#         'form': form,
#         'selected_category': category_filter,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/product/subcategory-admin.html", context)



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


# def attribute_admin(request):

#     attributes = Attribute.objects.all()
#     attribute_values = AttributeValue.objects.all()

#     context = {

#         'attributes':attributes,
#         'attribute_values':attribute_values,

#     }

#     return render(request, 'Al-admin/product/attribute-admin.html', context)


class AttributeListView(LoginRequiredMixin, ListView):
    model = Attribute
    template_name = 'Al-admin/product/attribute-admin.html'
    items_per_page = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search_query')
        attribute_id = self.request.GET.get('attribute_id')

        # Pagination for attributes
        attributes_query = Attribute.objects.all()
        if search_query:
            attributes_query = attributes_query.filter(
                name__icontains=search_query
            )
        paginator = Paginator(attributes_query, self.items_per_page)
        page_number = self.request.GET.get('page')
        try:
            attributes_page = paginator.page(page_number)
        except EmptyPage:
            attributes_page = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            attributes_page = paginator.page(1)

        context['attributes'] = attributes_page
        context['search_query'] = search_query

        # Pagination for attribute values
        if attribute_id:
            selected_attribute = Attribute.objects.get(pk=attribute_id)
            attribute_values_query = AttributeValue.objects.filter(attribute=selected_attribute)
            if search_query:
                attribute_values_query = attribute_values_query.filter(
                    Q(value__icontains=search_query) | Q(attribute__name__icontains=search_query)
                )
        else:
            attribute_values_query = AttributeValue.objects.all()

        paginator = Paginator(attribute_values_query, self.items_per_page)
        page_number = self.request.GET.get('attribute_value_page')
        try:
            attribute_values_page = paginator.page(page_number)
        except EmptyPage:
            attribute_values_page = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            attribute_values_page = paginator.page(1)

        context['selected_attribute'] = None if not attribute_id else selected_attribute
        context['attribute_values'] = attribute_values_page

        return context
    
    def dispatch(self, request, *args, **kwargs):
        user_has_permission = request.user.has_perm('products.view_attribute')

        # Check group permissions if user does not have direct permission
        if not user_has_permission:
            user_groups = request.user.groups.all()
            for group in user_groups:
                if group.permissions.filter(codename='view_attribute').exists():
                    user_has_permission = True
                    break

        if not user_has_permission:
            # Return some error or handle permission denial
            return render(request, 'Al-admin/permission/permission_denied.html')

        return super().dispatch(request, *args, **kwargs)


# category value based subcategory fetch function
@login_required
@csrf_exempt
def get_subcategories(request):
    if request.method == 'POST':
        print('axios post a value')
        data = json.loads(request.body)
        selected_category = data.get('selectedCategory')
        print(selected_category)
        subcategories = SubCategory.objects.filter(main_Category__name=selected_category)
        print(subcategories)
        subcategories_data = [{'name': subcategory.name, 'url_key': subcategory.url_Key} for subcategory in subcategories]
        return JsonResponse({'subcategories': subcategories_data})
    
# category value based brand fetch function
@login_required
@csrf_exempt
def get_brand(request):
    if request.method == 'POST':
        print('axios post a value')
        data = json.loads(request.body)
        selected_category = data.get('selectedCategory')
        print(selected_category)
        selectedsubCategory = data.get('selectedsubCategory')
        print(selectedsubCategory)
        # brand_instances = cat_subcat_brand_map.objects.filter(category__name=selected_category, sub_category__name=selectedsubCategory).values('brand__name', 'brand__id').distinct()
        # print(brand_instances)
        # brand_data = [{'name': brand['brand__name'], 'id': brand['brand__id']} for brand in brand_instances]
        # print(brand_data)
        # return JsonResponse({'brand': brand_data})


@login_required
@csrf_exempt
def add_new_attribute(request):
    if request.method == 'POST':
        # Extract attribute data from the POST request
        data = json.loads(request.body)
        name = data.get('name')
        slot_position = data.get('Slot_Position')
        active = data.get('Active')
        selected_subcategory_name = data.get('selectedsubCategory')

        # Validate and check if the attribute already exists
        if name and slot_position is not None and active:
            existing_attribute = Attribute.objects.filter(name=name).first()

            if existing_attribute:
                return JsonResponse({'status': 'error', 'message': 'Attribute with this name already exists.'})

            # Create a new attribute
            new_attribute = Attribute.objects.create(
                name=name,
                Slot_Position=int(slot_position),
                Active=bool(active)
            )

            if selected_subcategory_name:
                # Update Category_attribute_map based on the new attribute and subcategory
                selected_subcategory = SubCategory.objects.get(name=selected_subcategory_name)
                # category_attribute_map = Category_attribute_map.objects.create(
                #     subCategory=selected_subcategory,
                #     attribute=new_attribute,
                #     Slot_Position=int(slot_position),
                #     Active=bool(active)
                # )

                # Get all attributes for the selected subcategory
                # attributes = Category_attribute_map.objects.filter(subCategory__name=selected_subcategory_name)
                # attribute_values = [attribute.attribute.name for attribute in attributes]

                # return JsonResponse({'status': 'success', 'attribute_values': attribute_values})
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
@csrf_exempt
def update_attribute(request):
    if request.method == 'POST':
        # Extract data from the POST request
        # data = json.loads(request.body)

        try:
            attribute_id = request.POST.get('id')
            name = request.POST.get('attributeName')
            Slot_Position = request.POST.get('attributeSlot')
            Active = True if request.POST.get('active') == 'on' else False
            # Retrieve the attribute instance by ID
            attribute_instance = Attribute.objects.get(pk=attribute_id)

            # Update attribute instance
            attribute_instance.name = name
            attribute_instance.slot_position = int(Slot_Position)
            attribute_instance.active = Active
            attribute_instance.save()

            return JsonResponse({'status': 'success', 'message': 'Attribute updated successfully.'})
        except Attribute.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attribute not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# Function to delete an attribute
@login_required
@csrf_exempt
def delete_attribute(request, attribute_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the attribute instance by ID and delete it
            attribute_instance = Attribute.objects.get(pk=attribute_id)
            attribute_instance.delete()

            return JsonResponse({'status': 'success', 'message': 'Attribute deleted successfully.'})
        except Attribute.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attribute not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
@csrf_exempt
def add_new_attribute_value(request):
    if request.method == 'POST':
        # Extract data from the POST request
        data = json.loads(request.body)

        # Validate and create a new attribute value
        try:
            attribute_name = data['attribute']
            attribute_value = data['value']
            active = data.get('Active', False)

            # Check if the attribute value already exists
            if AttributeValue.objects.filter(attribute__name=attribute_name, value=attribute_value).exists():
                return JsonResponse({'status': 'error', 'message': 'Attribute value already exists.'})

            # Retrieve the attribute instance by name
            attribute_instance = Attribute.objects.get(name=attribute_name)

            # Create a new attribute value instance
            new_attribute_value = AttributeValue.objects.create(
                attribute=attribute_instance,
                value=attribute_value,
                Active=bool(active)
            )

            
            attribute_values = AttributeValue.objects.filter(attribute = attribute_instance)
            print(attribute_values)
            
            
            attr_values = ([{'name': attribute_values.value, 'attribute':attribute_values.attribute.name} for attribute_values in attribute_values])
            print(attr_values)
            return JsonResponse({'status': 'success', 'attributevalue':attr_values})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def update_attribute_value(request):
    if request.method == 'POST':
        # Extract data from the POST request
        # data = json.loads(request.body)

        try:
            attribute_value_id = request.POST.get('id')
            print(attribute_value_id)
            attribute = request.POST.get('updateattributeValueAttribute')
            print(attribute)
            attribute_value = request.POST.get('updateinputAttributeValue')
            print(attribute_value)
            attribute_value_active = True if request.POST.get('updateactiveAttributeValue') == 'on' else False

            attribute_instance = Attribute.objects.get(name=attribute)
            # Retrieve the attribute value instance by ID
            attribute_value_instance = AttributeValue.objects.get(pk=attribute_value_id)

            # Update attribute value instance
            attribute_value_instance.attribute = attribute_instance
            attribute_value_instance.value = attribute_value
            attribute_value_instance.active = attribute_value_active
            attribute_value_instance.save()

            return JsonResponse({'status': 'success', 'message': 'Attribute value updated successfully.'})
        except AttributeValue.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attribute value not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@csrf_exempt
def delete_attribute_value(request, attribute_value_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the attribute value instance by ID and delete it
            attribute_value_instance = AttributeValue.objects.get(pk=attribute_value_id)
            attribute_value_instance.delete()

            return JsonResponse({'status': 'success', 'message': 'Attribute value deleted successfully.'})
        except AttributeValue.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Attribute value not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



# subcategory selection based attribute fetch function
@login_required
def get_attribute(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selectedsubCategory = data.get('selectedsubCategory')
        print(selectedsubCategory)

        # attributes = Category_attribute_map.objects.filter(subCategory__name=selectedsubCategory)
        # print(attributes)

        Attributes = []

        # for attribute in attributes:
        #     Attributes.append({'attribute': attribute.attribute.name})  # Extract the attribute name

        return JsonResponse({'Attributes': Attributes})

    

# attribute base Attribute values fetch function

from django.http import JsonResponse
@login_required
def Attr_values(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        attribute = data.get('attribute')
        print(attribute)
        # Process the attribute data here...
        # You can perform database operations, calculations, or any other logic

        attr_values = []

        for attribute in attribute: 
            try:       
                # Create a sample response with attribute values
                attribute_values = AttributeValue.objects.filter(attribute__name = attribute)
                print(attribute_values)
            except Attribute.DoesNotExist:
                continue  # Skip this attribute if it doesn't exist
            
            # attr_values = [{'name': attribute_values.value, 'attribute':attribute_values.attribute} for attribute_values in attribute_values]
            attr_values.extend([{'name': attribute_values.value, 'attribute':attribute_values.attribute.name} for attribute_values in attribute_values])
        return JsonResponse({'attributevalue':attr_values})
    
    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Add new Category & subcategory & Brand
@login_required
def create_category(request):
    print('category axios post function work')
    if request.method == 'POST':
        print(request.POST)
        category_name = request.POST.get('name')
        description = request.POST.get('description')
        Slot_Position = request.POST.get('Slot_Position')

        # Convert checkbox values to boolean
        is_Active = True if request.POST.get('is_Active') == 'on' else False
        include_in_navigation_menu = True if request.POST.get('include_in_navigation_menu') == 'on' else False

        page_title = request.POST.get('page_title')
        meta_keyword = request.POST.get('meta_keyword')
        meta_description = request.POST.get('meta_description')

        # Get the uploaded image file
        category_img = request.FILES.get('category_img')

        # Check if a category with the same name already exists
        existing_category = ParentCategory.objects.filter(name=category_name).first()

        if existing_category:
            return JsonResponse({'message': 'Category already exists'})
        else:
            # Create the Category instance
            category = ParentCategory(
                name=category_name,
                description=description,
                is_Active=is_Active,
                include_in_navigation_menu=include_in_navigation_menu,
                Slot_Position=Slot_Position,
                page_Title=page_title,
                Meta_keyword=meta_keyword,
                Meta_description=meta_description,
            )

            # If image file is provided, save it
            if category_img:
                # Construct the file path where the image will be stored
                file_path = os.path.join('category', category_img.name)
                # Save the image file
                category.image.save(file_path, category_img, save=True)

            category.save()
            print(category)
            print('Category successfully saved')
            return JsonResponse({'message': 'Category created successfully'})

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('category successfully save')
            return JsonResponse({'message': 'Category created successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_category(request):
    if request.method == 'POST':
        print('axios post update category value')
        # Get the form data
        category_id = request.POST.get('category_id')
        print(category_id)
        category_name = request.POST.get('name')
        print(category_name)
        category_description = request.POST.get('description')
        print(category_description)
        slot_position = request.POST.get('slot_position')
        print(slot_position)
        is_active = True if request.POST.get('is_Active') == 'on' else False
        print(is_active)
        include_in_navigation_menu =True if request.POST.get('include_in_navigation_menu') == 'on' else False
        print(include_in_navigation_menu)

        page_title = request.POST.get(' page_title ')
        print(page_title)

        meta_keyword = request.POST.get('meta_keyword_update')
        print(meta_keyword)

        meta_description = request.POST.get('meta_description_update')
        print(meta_description)

        category_img = request.POST.get('category_img')
        print(category_img)

        if category_img:
            category_img = os.path.join('category', category_img.strip('/'))

        category_update = ParentCategory.objects.get(id=category_id)
        print(category_update)

        category_update.name = category_name
        category_update.description = category_description
        category_update.active = is_active
        category_update.include_in_navigation_menu= include_in_navigation_menu
        category_update.slot_position = slot_position
        if category_img:
            category_update.image = category_img
        category_update. page_title  = page_title
        category_update.meta_keyword = meta_keyword
        category_update.meta_description  = meta_description

        category_update.save()

        # Return a JSON response indicating the success or failure of the update
        return JsonResponse({'success': True, 'message': 'category updated successfully'})

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'message': 'Invalid request'}, status=400)

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

@login_required
def create_subcategory(request):
    print('subcategory axios post function work')
    if request.method == 'POST':
        print(request.POST)
        main_Category = request.POST.get('parent_category')
        print(main_Category)
        subcategory_name = request.POST.get('name')
        description = request.POST.get('description')
        Slot_Position = request.POST.get('Slot_Position')

        is_Active = True if request.POST.get('is_Active') == 'on' else False
        include_in_navigation_menu = True if request.POST.get('include_in_navigation_menu') == 'on' else False

        page_title = request.POST.get('page_title')
        print(page_title)

        meta_keyword = request.POST.get('meta_keyword')
        print(meta_keyword)

        meta_description = request.POST.get('meta_description')
        print(meta_description)

        category_img = request.FILES.get('image')
        print(category_img)

        try:
            category_instance = ParentCategory.objects.get(name=main_Category)
            print(category_instance)
        except ParentCategory.DoesNotExist:
            print('category not available')
            return JsonResponse({'message': 'Category does not exist'})

        existing_subcategory = SubCategory.objects.filter(name=subcategory_name).first()
        print(existing_subcategory)

        if existing_subcategory:
            return JsonResponse({'message': 'Subcategory already exists'})
        else:
            print('Subcategory creation')
            subcategory = SubCategory(
                main_Category=category_instance,
                name=subcategory_name,
                description=description,
                is_Active=is_Active,
                include_in_navigation_menu=include_in_navigation_menu,
                Slot_Position=Slot_Position,
                image=category_img,
                page_Title=page_title,
                Meta_keyword=meta_keyword,
                Meta_description=meta_description,
            )
            subcategory.save()
            print(subcategory)
            print('Subcategory successfully saved')
            return JsonResponse({'message': 'Subcategory created successfully', 'subcategory': subcategory.name})

    
    # if request.method == 'POST':
    #     form = SubCategoryForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         print('subcategory successfully save')
    #         return JsonResponse({'message': 'Subcategory created successfully'})
    #     else:
    #         return JsonResponse({'error': form.errors}, status=400)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_subcategory(request):
    if request.method == 'POST':
        print('axios post update category value')
        # Get the form data
        main_Category = request.POST.get('main_Category')
        print(main_Category)
        subcategory_id = request.POST.get('subcategory_id')
        print(subcategory_id)
        subcategory_name = request.POST.get('name')
        print(subcategory_name)
        subcategory_description = request.POST.get('description')
        print(subcategory_description)
        slot_position = request.POST.get('Slot_Position')
        print(slot_position)
        is_active = True if request.POST.get('is_Active') == 'on' else False
        print(is_active)
        include_in_navigation_menu =True if request.POST.get('include_in_navigation_menu') == 'on' else False
        print(include_in_navigation_menu)

        page_title = request.POST.get('page_title')
        print(page_title)

        meta_keyword = request.POST.get('meta_keyword_update')
        print(meta_keyword)

        meta_description = request.POST.get('meta_description_update')
        print(meta_description)

        subcategory_img = request.POST.get('subcategory_img')
        print(subcategory_img)

        if subcategory_img:
            subcategory_img = os.path.join('category', subcategory_img.strip('/'))

        # Find the corresponding category instance based on the provided category name
        try:
            print('try function check ')
            category_instance = ParentCategory.objects.get(name=main_Category)
            print(category_instance)
        except ParentCategory.DoesNotExist:
            print('category not available')
            return JsonResponse({'message': 'category does not exist'})

        subcategory_update = SubCategory.objects.get(id=subcategory_id)
        print(subcategory_update)

        subcategory_update.parent_category= category_instance
        subcategory_update.name = subcategory_name
        subcategory_update.description = subcategory_description
        subcategory_update.active = is_active
        subcategory_update.include_in_navigation_menu = include_in_navigation_menu
        subcategory_update.slot_position = slot_position
        subcategory_update.image = subcategory_img
        subcategory_update.page_title = page_title
        subcategory_update. meta_keyword = meta_keyword
        subcategory_update.meta_description = meta_description

        subcategory_update.save()

        # Return a JSON response indicating the success or failure of the update
        return JsonResponse({'success': True, 'message': 'Brand updated successfully'})

    # Handle other HTTP methods or invalid requests
    return JsonResponse({'message': 'Invalid request'}, status=400)

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



@login_required
def create_brand(request):
    print('brand axios post function work')
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        print(name)
        brand_image = request.FILES.get('image')

        # Convert checkbox values to boolean
        Active = True if request.POST.get('active') == 'on' else False

        category = request.POST.get('catagory')
        print(category)

        sub_category = request.POST.get('sub_category')
        print(sub_category)

        # Check if a brand with the same name already exists
        existing_brand = Brand.objects.filter(name=name).first()
        print(existing_brand)        

        if existing_brand:
            return JsonResponse({'message': 'Brand already exists'})

        else:
            # if brand_image:
            #     brand_image = os.path.join('brand', brand_image.strip('/'))
            #     print(brand_image)

            brand = Brand(
                name=name,
                brand_image=brand_image,
                active=Active,
            )
            # If image file is provided, save it
            if brand_image:
                # Construct the file path where the image will be stored
                file_path = os.path.join('brand', brand_image.name)
                # Save the image file
                brand.brand_image.save(file_path, brand_image, save=True)
            brand.save()
            print(brand)

            category_instance = None
            subcategory_instance = None

            if category:  # If there is a category selected
                category_instance = ParentCategory.objects.get(name=category)
                print(category_instance)

            if sub_category:  # If there is a subcategory selected
                subcategory_instance = SubCategory.objects.get(name=sub_category)
                print(subcategory_instance)

            if category_instance and subcategory_instance:
                print('cate_sub_map add function')
                # cat_subcat_brand_map_instance = cat_subcat_brand_map(
                #     brand=brand,
                #     category=category_instance,
                #     sub_category=subcategory_instance,
                # )
                # cat_subcat_brand_map_instance.save()
                # print(cat_subcat_brand_map_instance)

            print('Brand successfully saved')

            # Prepare the data to be sent in the JsonResponse
            brand_data = {
                'id': brand.pk,
                'name': brand.name,
            }

            return JsonResponse({'message': 'Brand created successfully', 'brand_data': brand_data})
# def create_brand(request):
#     print('brand axios post function work')
#     if request.method == 'POST':
#         print(request.POST)
#         name = request.POST.get('name')
#         print(name)
#         brand_image = request.POST.get('brand_image')

#         # Convert checkbox values to boolean
#         Active = True if request.POST.get('Active') == 'on' else False

#         category = request.POST.get('catagory')
#         print(category)

#         sub_category = request.POST.get('sub_category')
#         print(sub_category)

#         # Check if a category with the same name already exists
#         existing_brand = Brand.objects.filter(name=name).first()
#         print(existing_brand)        

#         if existing_brand:
#             return JsonResponse({'message': 'Brand already exist'})
        

#         else:
#             if brand_image:
#                 brand_image = os.path.join('brand', brand_image.strip('/'))
#                 print(brand_image)

#             brand = Brand(
#                 name = name,
#                 brand_image = brand_image,
#                 Active = Active,
#             )
#             # brand.save()
#             print(brand)

#             if category:  # If there is no catagory show
#                 category_instance = Category.objects.get(name = category)
#                 print(category_instance)
#             if sub_category :
#                 subCategory_instance = subCategory.objects.get(name=sub_category)
#                 print(subCategory_instance)

#             cat_subcat_brand_map_instance = cat_subcat_brand_map(
#                 brand=brand,
#                 category=category_instance,
#                 sub_category=subCategory_instance,
#             )
#             # cat_subcat_brand_map_instance.save()
#             print(cat_subcat_brand_map_instance)

#         print('Brand successfully save')
#         return JsonResponse({'message': 'Brand created successfully'})


    # if request.method == 'POST':
    #     form = BrandForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         print('brand successfully save')
    #         return JsonResponse({'message': 'Brand created successfully'})
    #     else:
    #         return JsonResponse({'error': form.errors}, status=400)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
@csrf_exempt  # Use csrf_exempt to disable CSRF protection for this view, or use a proper CSRF solution
def update_brand(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            brand_id = request.POST.get('brand_id')
            name = request.POST.get('name')
            Active = True if request.POST.get('active') == 'on' else False
            brand_image = request.POST.get('brand_image')

            # Retrieve the existing brand
            brand = Brand.objects.get(id=brand_id)

            # Update the brand data
            brand.name = name

            # Check if a new image file was uploaded
            if brand_image:
                brand_image = os.path.join('brand', brand_image.strip('/'))
                brand.brand_image = brand_image
                print('Brand Image Update successfully')

            brand.Active = Active
            brand.save()

            print('Brand successfully updated')

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Brand updated successfully'})
        except Brand.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Brand not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    # Return an error response for non-POST requests
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


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



# Export Excel Sheet 
@login_required
def export_to_xls(request):

    # Define the response content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the CSV header row
    headers = ['product_name', 'product_sku', 'brand_name', 'category_name', 'sub_category_name', 'description', 'short_description', 'warranty_conditions', 'regular_price ', 'sale_price ', 'weight', 'stock', 'in_stock', 'images', 'attributes', 'attribute_values']
    writer.writerow(headers)

    # Query the products data
    product_data = Product.objects.all()

    # Write product data to the CSV
    for product in product_data:
        # Write only the image file names to the CSV
        images = ','.join([os.path.basename(image.image.url) for image in product.images.all()])

        # Get attributes and attribute values as comma-separated strings
        attributes = ','.join([attr_value.attribute.name for attr_value in product.attribute_values.all()])
        attribute_values = ','.join([attr_value.attribute_value.value for attr_value in product.attribute_values.all()])

        row = [
            product.name,
            # product.model_number,
            product.sku,
            # product.product_Video,
            product.brands.name if product.brands else '',
            product.categories.name if product.categories else '',
            product.subcategories.name if product.subcategories else '',
            product.description,
            product.short_description if product.short_description else '',
            # product.warranty_conditions if product.warranty_conditions else '',
            product.regular_price,
            product.sale_price  if product.sale_price else '',
            product.weight if product.weight else '',
            product.stock,
            product.in_stock,
            images,
            attributes,
            attribute_values
        ]
        writer.writerow(row)
    return response
   




    # Prepare the HTTP response
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="products.csv"'

    # # Create a CSV writer
    # csv_writer = csv.writer(response)

    # # Write headers
    # headers = ['product_name', 'model_number', 'product_sku', 'product_Image1', 'product_Image2', 'product_Image3', 'product_Image4', 'product_Video', 'brand_name', 'category_name', 'sub_category_name', 'description', 'short_description', 'warranty_conditions', 'price', 'special_price', 'weight', 'stock', 'in_stock']
    # csv_writer.writerow(headers)

    # # Query the products data
    # product_data = products.objects.all()

    # # Write product data to the CSV
    # for product in product_data:
    #     csv_writer.writerow([
    #         product.product_name,
    #         product.model_number,
    #         product.product_sku,
    #         product.product_Image1.url if product.product_Image1 else '',
    #         product.product_Image2.url if product.product_Image2 else '',
    #         product.product_Image3.url if product.product_Image3 else '',
    #         product.product_Image4.url if product.product_Image4 else '',
    #         product.product_Video,
    #         product.brand.name if product.brand else '',
    #         product.category.name if product.category else '',
    #         product.sub_category.name if product.sub_category else '',
    #         product.description,
    #         product.short_description if product.short_description else '',
    #         product.warranty_conditions if product.warranty_conditions else '',
    #         product.price,
    #         product.special_price if product.special_price else '',
    #         product.weight if product.weight else '',
    #         product.stock,
    #         product.in_stock,
    #     ])

    # return response

    # # Create a new Excel workbook and add a sheet
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('Products')
    # # Add headers to the sheet
    # headers = ['product_name', 'model_number', 'product_sku', 'product_Image1', 'product_Image2', 'product_Image3', 'product_Image4', 'product_Video', 'brand_name', 'category_name', 'sub_category_name', 'description', 'short_description', 'warranty_conditions', 'price', 'special_price', 'weight', 'stock', 'in_stock']
    # # Write the headers to the sheet
    # for col, header in enumerate(headers):
    #     sheet.write(0, col, header)

    #     # Query the products data
    #     product_data = products.objects.all()

    #     # Write product data to the sheet
    #     for row_idx, product in enumerate(product_data, start=1):
    #         sheet.write(row_idx, 0, product.product_name)
    #         sheet.write(row_idx, 1, product.model_number)
    #         sheet.write(row_idx, 2, product.product_sku)
    #         sheet.write(row_idx, 3, product.product_Image1.url if product.product_Image1 else '')
    #         sheet.write(row_idx, 4, product.product_Image2.url if product.product_Image2 else '')
    #         sheet.write(row_idx, 5, product.product_Image3.url if product.product_Image3 else '')
    #         sheet.write(row_idx, 6, product.product_Image4.url if product.product_Image4 else '')
    #         sheet.write(row_idx, 7, product.product_Video)
    #         sheet.write(row_idx, 8, product.brand.name if product.brand else '')
    #         sheet.write(row_idx, 9, product.category.name if product.category else '')
    #         sheet.write(row_idx, 10, product.sub_category.name if product.sub_category else '')
    #         sheet.write(row_idx, 11, product.description)
    #         sheet.write(row_idx, 12, product.short_description if product.short_description else '')
    #         sheet.write(row_idx, 13, product.warranty_conditions if product.warranty_conditions else '')
    #         sheet.write(row_idx, 14, product.price)
    #         sheet.write(row_idx, 15, product.special_price if product.special_price else '')
    #         sheet.write(row_idx, 16, product.weight if product.weight else '')
    #         sheet.write(row_idx, 17, product.stock)
    #         sheet.write(row_idx, 18, product.in_stock)

    #     # Create an HTTP response with the XLS content
    #     # For example, you could use the HttpResponse to return a downloadable XLS file
    #     response = HttpResponse(content_type='application/ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="products.xls"'
    #     # Save the workbook to the response
    #     workbook.save(response)
    #     return response
    
@login_required
def download_sample_xls(request):
    # sample CSV file
    file_path = 'media/sample_products_data.csv'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sample_products_data.csv"'
            return response
    else:
        return HttpResponse("Sample CSV file not found.", status=404)
    # file_path = 'media/sample_products_data.xls'
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as file:
    #         response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
    #         response['Content-Disposition'] = 'attachment; filename="sample_products_data.xls"'
    #         return response
    # else:
    #     return HttpResponse("Sample XLS file not found.", status=404)

@login_required   
def import_product(request):
    print('Product Import Function')
    if request.method == "POST" and request.FILES['csv_file']:
        print('Post functino is work')
        try:
            file = request.FILES["csv_file"]
            if not file.name.endswith(('.csv', '.xls', '.xlsx')):
                return HttpResponse("Invalid file format. Please upload a CSV or Excel file.")

            if file.name.endswith('.csv'):
                data = file.read().decode("utf-8")
                csv_data = csv.reader(data.splitlines())

                # Read and skip the header row
                header = next(csv_data)

                for row in csv_data:
                    # Assuming xls columns are in the order of product_name, model_number, product_sku, product_Video, brand_name, category_name, sub_category_name, description, short_description, warranty_conditions, price, special_price, weight, stock, in_stock, images, attributes, attribute_values
                    product_name, model_number, product_sku, product_Video, brand_name, category_name, sub_category_name, description, short_description, warranty_conditions, regular_price, sale_price , weight, stock, in_stock, images, attributes, attribute_values = row[:18]


                    images = images.split(",")
                    print(images)

                    attributes = attributes.split(',')  # Split attribute values by comma
                    attribute_values = attribute_values.split(',')  # Split attribute value values by comma

                    # Ensure that the number of attributes and values match
                    if len(attributes) != len(attribute_values):
                        print(f"Error: Number of attributes and values do not match for SKU: {product_sku}")
                        print(f"Row: {row}")
                        print(f"Attributes: {attributes}")
                        print(f"Attribute Values: {attribute_values}")
                        return HttpResponseServerError("Number of attributes and values do not match for SKU: {}".format(product_sku))
                        # Check if required fields are empty
                        # if not all([category_name, sub_category_name, brand_name, in_stock]):
                        #     raise ValueError("One or more required fields are empty in this row.")

                        # Create a list to store the names of empty fields
                    empty_fields = []

                    # Check if required fields are empty
                    if not category_name:
                        empty_fields.append("Category")
                    if not sub_category_name:
                        empty_fields.append("Sub-Category")
                    if not brand_name:
                        empty_fields.append("Brand")
                    if not in_stock:
                        empty_fields.append("Stock Status")

                    if empty_fields:
                        error_message = f"The following required fields are empty in this row: {', '.join(empty_fields)}."
                        return HttpResponseServerError(error_message)
                        
                    # Find or create Brand, Category, and SubCategory instances
                    brand, _ = Brand.objects.get_or_create(name=brand_name)

                    # First, find or create the Category instance
                    category, _ = ParentCategory.objects.get_or_create(name=category_name)

                    # Then, create the SubCategory instance with the Category as its main_Category
                    sub_category, _ = SubCategory.objects.get_or_create(main_Category=category, name=sub_category_name)



                    # Convert the empty strings to None
                    price = regular_price if regular_price else None
                    special_price = sale_price  if sale_price  else None
                    weight = weight if weight else None

                        

                    # Check if the product with the given SKU already exists
                    product, created = Product.objects.get_or_create(product_sku=product_sku, defaults={
                        'product_name': product_name,
                        'model_number': model_number,
                        'product_Video': product_Video,
                        'brand': brand,
                        'category': category,
                        'sub_category': sub_category,
                        'description': description,
                        'short_description': short_description,
                        # 'warranty_conditions': warranty_conditions,
                        'regular_price': price,
                        'special_price': special_price,
                        'weight': weight,
                        'stock': stock,
                        'in_stock': in_stock,
                    })

                    # Update the product details if it already exists
                    if not created:
                        product.name = product_name
                        # product.model_number = model_number
                        # product.product_Video = product_Video
                        product.brands = brand
                        product.categories = category
                        product.subcategories = sub_category
                        product.description = description
                        product.short_description = short_description
                        # product.warranty_conditions = warranty_conditions
                        product.regular_price = price
                        product.sale_price = special_price
                        product.weight = weight
                        product.stock = stock
                        product.in_stock = in_stock
                        product.save()

                    # Upload product images
                    existing_images = set(ProductImage.objects.filter(product=product).values_list('image', flat=True))

                    for image_path in images:
                        image_path = image_path.strip()
                        if image_path:
                            image_path = os.path.join('product', image_path.strip('/'))

                            # Check if the image already exists for the product
                            product_image_instance = ProductImage.objects.filter(product=product, image=image_path).first()

                            if product_image_instance:
                                # Update the existing image instance
                                product_image_instance.image = image_path
                                product_image_instance.save()
                            else:
                                # Create a new image instance
                                product_image_instance = ProductImage.objects.create(
                                    product=product,
                                    image=image_path
                                )
                                print(f'New image added for product {product.name}: {image_path}')

                    # Delete extra images not present in the updated CSV
                    extra_images = existing_images - set(images)
                    for extra_image_path in extra_images:
                        extra_image_path = os.path.join('product', extra_image_path.strip('/'))
                        ProductImage.objects.filter(product=product, image=extra_image_path).delete()
                        print(f'Deleted extra image: {extra_image_path}')


                    for attribute_name, attribute_value in zip(attributes, attribute_values):
                        # Check if both attribute and attribute_value are not empty
                        if attribute_name.strip() and attribute_value.strip():
                            # Check if Attribute exists or create new
                            attribute, created = Attribute.objects.get_or_create(name=attribute_name.strip())

                            # Check if AttributeValue exists or create new
                            attribute_value_name = attribute_value.strip()
                            attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_value_name, Active=True)

                            # Check if Category_attribute_map exists or create new
                            # category_attribute_map, created = Category_attribute_map.objects.get_or_create(
                            #     subCategory=sub_category,
                            #     attribute=attribute,
                            #     Active=True
                            # )

                            # Retrieve product ID based on product SKU
                            # product = products.objects.get(product_sku=product_sku)

                            # Check if product_attr_values_map exists or create new
                            # product_attr_value_map, created = product_attr_values_map.objects.get_or_create(
                            #     product=product,
                            #     subcategory=sub_category,
                            #     attribute=attribute,
                            #     attribute_value=attribute_value,
                            #     Active=True
                            # )

                            # print(product_attr_value_map)
                        else:
                            print("Skipping empty attribute and attribute_value")
            return JsonResponse({"success": "Products imported successfully."})

        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"})

    form = CsvImportForm()
    data = {"form": form}

    return render(request, "Al-admin/product/import_product_csv.html")

@login_required
def update_product(request):
    print('Product Update Function')
    if request.method == "POST" and request.FILES['csv_file']:
        print('Post functino is work')
        try:
            file = request.FILES["csv_file"]
            if not file.name.endswith(('.csv', '.xls', '.xlsx')):
                return HttpResponse("Invalid file format. Please upload a CSV or Excel file.")

            if file.name.endswith('.csv'):
                data = file.read().decode("utf-8")
                csv_data = csv.reader(data.splitlines())

                # Read and skip the header row
                header = next(csv_data)

                for row in csv_data:
                    # Assuming xls columns are in the order of product_name, model_number, product_sku, product_Video, brand_name, category_name, sub_category_name, description, short_description, warranty_conditions, price, special_price, weight, stock, in_stock, images, attributes, attribute_values
                    product_name,  product_sku,  brand_name, category_name, sub_category_name, description, short_description,  regular_price , sale_price , weight, stock, in_stock= row[:15]


                    # images = images.split(",")
                    # print(images)

                    # attributes = attributes.split(',')  # Split attribute values by comma
                    # attribute_values = attribute_values.split(',')  # Split attribute value values by comma

                    # # Ensure that the number of attributes and values match
                    # if len(attributes) != len(attribute_values):
                    #     print(f"Error: Number of attributes and values do not match for SKU: {product_sku}")
                    #     print(f"Row: {row}")
                    #     print(f"Attributes: {attributes}")
                    #     print(f"Attribute Values: {attribute_values}")
                    #     return HttpResponseServerError("Number of attributes and values do not match for SKU: {}".format(product_sku))
                    #     # Check if required fields are empty
                    #     # if not all([category_name, sub_category_name, brand_name, in_stock]):
                    #     #     raise ValueError("One or more required fields are empty in this row.")

                        # Create a list to store the names of empty fields
                    empty_fields = []

                    # Check if required fields are empty
                    if not category_name:
                        empty_fields.append("Category")
                    if not sub_category_name:
                        empty_fields.append("Sub-Category")
                    if not brand_name:
                        empty_fields.append("Brand")
                    if not in_stock:
                        empty_fields.append("Stock Status")

                    if empty_fields:
                        error_message = f"The following required fields are empty in this row: {', '.join(empty_fields)}."
                        return HttpResponseServerError(error_message)
                        
                    # Find or create Brand, Category, and SubCategory instances
                    brand, _ = Brand.objects.get_or_create(name=brand_name)

                    # First, find or create the Category instance
                    category, _ = ParentCategory.objects.get_or_create(name=category_name)

                    # Then, create the SubCategory instance with the Category as its main_Category
                    sub_category, _ = SubCategory.objects.get_or_create(main_Category=category, name=sub_category_name)



                    # Convert the empty strings to None
                    price = regular_price  if regular_price else None
                    special_price = sale_price  if sale_price  else None
                    weight = weight if weight else None

                        

                    # Check if the product with the given SKU already exists
                    product, created = Product.objects.get_or_create(product_sku=product_sku, defaults={
                        'product_name': product_name,
                        # 'model_number': model_number,
                        # 'product_Video': product_Video,
                        'brand': brand,
                        'category': category,
                        'sub_category': sub_category,
                        'description': description,
                        'short_description': short_description,
                        # 'warranty_conditions': warranty_conditions,
                        'regular_price ': price,
                        'special_price': special_price,
                        'weight': weight,
                        'stock': stock,
                        'in_stock': in_stock,
                    })

                    # Update the product details if it already exists
                    if not created:
                        product.name = product_name
                        # product.model_number = model_number
                        # product.product_Video = product_Video
                        product.brands = brand
                        product.categories  = category
                        product. subcategories  = sub_category
                        product.description = description
                        product.short_description = short_description
                        # product.warranty_conditions = warranty_conditions
                        product.regular_price  = price
                        product.sale_price = special_price
                        product.weight = weight
                        product.stock = stock
                        product.in_stock = in_stock
                        product.save()

                    # Upload product images
                    # existing_images = set(product_image.objects.filter(product=product).values_list('image', flat=True))

                    # for image_path in images:
                    #     image_path = image_path.strip()
                    #     if image_path:
                    #         image_path = os.path.join('product', image_path.strip('/'))

                    #         # Check if the image already exists for the product
                    #         product_image_instance = product_image.objects.filter(product=product, image=image_path).first()

                    #         if product_image_instance:
                    #             # Update the existing image instance
                    #             product_image_instance.image = image_path
                    #             product_image_instance.save()
                    #         else:
                    #             # Create a new image instance
                    #             product_image_instance = product_image.objects.create(
                    #                 product=product,
                    #                 image=image_path
                    #             )
                    #             print(f'New image added for product {product.product_name}: {image_path}')

                    # # Delete extra images not present in the updated CSV
                    # extra_images = existing_images - set(images)
                    # for extra_image_path in extra_images:
                    #     extra_image_path = os.path.join('product', extra_image_path.strip('/'))
                    #     product_image.objects.filter(product=product, image=extra_image_path).delete()
                    #     print(f'Deleted extra image: {extra_image_path}')


                    # for attribute_name, attribute_value in zip(attributes, attribute_values):
                    #     # Check if both attribute and attribute_value are not empty
                    #     if attribute_name.strip() and attribute_value.strip():
                    #         # Check if Attribute exists or create new
                    #         attribute, created = Attribute.objects.get_or_create(name=attribute_name.strip())

                    #         # Check if AttributeValue exists or create new
                    #         attribute_value_name = attribute_value.strip()
                    #         attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_value_name, Active=True)

                    #         # Check if Category_attribute_map exists or create new
                    #         category_attribute_map, created = Category_attribute_map.objects.get_or_create(
                    #             subCategory=sub_category,
                    #             attribute=attribute,
                    #             Active=True
                    #         )

                    #         # Retrieve product ID based on product SKU
                    #         # product = products.objects.get(product_sku=product_sku)

                    #         # Check if product_attr_values_map exists or create new
                    #         product_attr_value_map, created = product_attr_values_map.objects.get_or_create(
                    #             product=product,
                    #             subcategory=sub_category,
                    #             attribute=attribute,
                    #             attribute_value=attribute_value,
                    #             Active=True
                    #         )

                    #         print(product_attr_value_map)
                    #     else:
                    #         print("Skipping empty attribute and attribute_value")
            return JsonResponse({"success": "Products Update successfully."})

        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"})

    form = CsvImportForm()
    data = {"form": form}

    return render(request, "Al-admin/product/update_product_csv.html")


@login_required
def order_page(request):
    order = Order.objects.all().order_by('-order_date').values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date')
    print(order)
    all_order_count = order.count()
    print(all_order_count)
    payment_Pending_count = order.filter(payment_status='Pending').count()
    print(payment_Pending_count)

    order_delivered_count = order.filter(order_status='Delivered').count()
    print(order_delivered_count)

    order_cancelled_count = order.filter(order_status='Cancelled').count()
    print(order_cancelled_count)

    order_shipped_count = order.filter(order_status='Shipped').count()
    print(order_shipped_count)

    # order_status = Status.objects.all()
    # print(order_status)

    # payment_type = payment_method.objects.all()
    # print(payment_type)


    user_has_permission = request.user.has_perm('checkout.view_Order')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_Order').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')


    context = {
        'order':order,
        'all_order_count':all_order_count,
        'payment_Pending_count':payment_Pending_count,
        'order_delivered_count':order_delivered_count,
        'order_cancelled_count':order_cancelled_count,
        'order_shipped_count':order_shipped_count,
        # 'order_status':order_status,
        # 'payment_type':payment_type,
    }
    return render(request, 'Al-admin/order/order.html', context )

@login_required
def order_replacement_page(request):
    order = Order.objects.filter(order_status = 'Replacement').order_by('-order_date').values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date')
    print(order)

    # replace_status = ReplacementStatusUpdate.objects.filter(order=order)

    # processing = ReplacementStatusUpdate.objects.filter(status='Processing').count()
    # print(processing)

    # Assign_agent = ReplacementStatusUpdate.objects.filter(status='Assign To Agent').count()
    # print(Assign_agent)

    # Approved = ReplacementStatusUpdate.objects.filter(status='Approved').count()
    # print(Approved)

    # Delivered = ReplacementStatusUpdate.objects.filter(status='Delivered').count()
    # print(Delivered)

    # Cancelled = ReplacementStatusUpdate.objects.filter(status='Canceled').count()
    # print(Cancelled)
    

    # order_status = Status.objects.all()
    # print(order_status)

    # payment_type = payment_method.objects.all()
    # print(payment_type)


    user_has_permission = request.user.has_perm('checkout.view_orderreplacementcomment')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_orderreplacementcomment').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    


    context = {
        'order':order,
        # # 'all_order_count':all_order_count,
        # 'processing':processing,
        # 'Assign_agent':Assign_agent,
        # 'Approved':Approved,
        # 'Delivered':Delivered,
        # 'Cancelled':Cancelled,
        # 'order_status':order_status,
        # 'payment_type':payment_type,
    }
    return render(request, 'Al-admin/order/order_replace.html', context )

@login_required
def order_details(request, order_id):

    user = request.user
    print(order_id)
    order = Order.objects.get(order_id = order_id)
    print(order)

    # Retrieve order items
    order_item = OrderItem.objects.filter(order_id=order.id) 


    # get the OrderItem objects related to the order
    order_items = order.OrderItem_set.all()
    print(order_items)
    print(order.Billing_address)

    Billing_address =  Address.objects.values().filter(id=order.Billing_address.id)
    print(Billing_address)

    Shipping_address =  Address.objects.values().filter(id=order.shipping_address.id)
    print(Shipping_address)
    
    # userorder = get_object_or_404(Order, order_id= order_id)
    
    invoice = Invoice.objects.get(order_id = order)
    print(invoice)
    print('invoice id of order sucess page')

    # order_Status = Status.objects.all()

    # try:
    #     delivery_person_details = OrderDeliveryPerson.objects.get(order=order)
    # except OrderDeliveryPerson.DoesNotExist:
    #     delivery_person_details = None

        
    user_has_permission = request.user.has_perm('checkout.view_Order')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_Order').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'order': order,
        'order_items':order_items,
        'user': user,
        'order_id': order_id,
        'Billing_address':Billing_address,
        'Shipping_address':Shipping_address,
        'invoice':invoice,
        # 'order_Status':order_Status,
        # 'delivery_person_details':delivery_person_details,
        
    }

    return render(request, 'Al-admin/order/order_details.html', context)

@login_required
def order_replacement_details(request, order_id):

    user = request.user
    print(order_id)
    order = Order.objects.get(order_id = order_id)
    print(order)

    # Retrieve order items
    order_item = OrderItem.objects.filter(order_id=order.id) 


    # get the OrderItem objects related to the order
    order_items = order.OrderItem_set.all()
    print(order_items)
    print(order.Billing_address)

    Billing_address =  Address.objects.values().filter(id=order.Billing_address.id)
    print(Billing_address)

    Shipping_address =  Address.objects.values().filter(id=order.shipping_address.id)
    print(Shipping_address)
    
    # userorder = get_object_or_404(Order, order_id= order_id)
    
    invoice = Invoice.objects.get(order_id = order)
    print(invoice)
    print('invoice id of order sucess page')

    # order_Status = Status.objects.all()

    # order_replace_Status = ReplacementStatusUpdate.objects.get(order = order)
    # print(order_replace_Status)

    # try:
    #     collect_person = ReplacementCollectPerson.objects.get(order=order)
    #     print(collect_person)
    # except ReplacementCollectPerson.DoesNotExist:
    #     # Handle the case when ReplacementCollectPerson does not exist for the given order
    #     collect_person = None
    #     print("ReplacementCollectPerson does not exist for this order")

    # replace_reason = OrderReplacementComment.objects.get(order=order)

    user_has_permission = request.user.has_perm('checkout.view_orderreplacementcomment')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_orderreplacementcomment').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    


    context = {
        'order': order,
        'order_items':order_items,
        'user': user,
        'order_id': order_id,
        'Billing_address':Billing_address,
        'Shipping_address':Shipping_address,
        'invoice':invoice,
        # 'order_Status':order_Status,
        # 'order_replace_Status':order_replace_Status,
        # 'collect_person':collect_person,
        # 'replace_reason':replace_reason,
        
    }

    return render(request, 'Al-admin/order/order_replace_details.html', context)

@login_required
def order_filter_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        filter_type = data.get('filter_type')
        filter_value = data.get('filter_value')

        order = Order.objects.all()

        if filter_type == 'order_status':
            order = order.values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date').filter(order_status=filter_value)
        elif filter_type == 'payment_status':
            order = order.values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date').filter(payment_status=filter_value)
        else:
           order = order.values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date').filter(payment_method__payment_name=filter_value)
        
        print(order)
        # Convert the QuerySet to a list
        order_data = list(order)
        # serialized_data = serializers.serialize('json', product)
    
        return JsonResponse(order_data, safe=False)


# @login_required
# def send_cancel_email(user_email, order_id, comment):
#     try:
#         print('send_cancel_email mail is working data pass also work')
#         subject = 'Your Replacement Request Has Been Canceled'
#         template_name = 'replacement_cancel_email.html'  # Create an HTML template for the email

#         # Extract the email address from the User object
#         if isinstance(user_email, User):
#             user_email = user_email.email

#         # Context data for the email template
#         context = {
#             'order_id': order_id,
#             'user': user_email,
#             'comment': comment,  # Pass the comment to the email template
#         }

#         # Render the HTML content of the email template
#         html_message = render_to_string(template_name, context)

#         # Remove HTML tags for the plain text version of the email
#         plain_message = strip_tags(html_message)

#         # Send the email
#         send_mail(
#             subject,
#             plain_message,
#             'onlineorders@suwaidillc.ae',  # Replace with your sender email address
#             [user_email],
#             html_message=html_message,
#         )
#     except Exception as e:
#         print(f"Exception occurred in send_cancel_email: {e}")



@login_required
def replace_order_status_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        replace_order_status = data.get('replace_order_status')
        print(replace_order_status)
        order_id = data.get('order_id')
        print(order_id)
        canceledComment = data.get('canceledComment')
        print(canceledComment)

        # Assuming you have an order object that you want to update
        # replace_order = ReplacementStatusUpdate.objects.get(order__order_id=order_id)

        # Update the order status
        # replace_order.status = replace_order_status
        # replace_order.save()

        if canceledComment:
            subject = 'Your Replacement Request Has Been Canceled'
            template_name = 'replacement_cancel_email.html'  # Create an HTML template for the email

            
            # user_email = replace_order.user

            # Context data for the email template
            context = {
                'order_id': order_id,
                # 'user': user_email,
                'comment': canceledComment,  # Pass the comment to the email template
            }

            # Render the HTML content of the email template
            html_message = render_to_string(template_name, context)

            # Remove HTML tags for the plain text version of the email
            # plain_message = strip_tags(html_message)

            # Send the email
            send_mail(
                subject,
                # plain_message,
                'onlineorders@suwaidillc.ae',  # Replace with your sender email address
                # [user_email],
                html_message=html_message,
            )
            print('Cancel mail send sucessfully')

        # Return a response, e.g., a success message or updated order details
        # response_data = {'message': 'Order replacement status updated successfully', 'order_status': replace_order.status}
        # return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest('Invalid request method')



@login_required
def send_user_notification_email(user_email, collect_person):
    print(user_email)
    print(collect_person)
    subject = 'Replacement Product Collect Person Assignment'
    message = render_to_string('collect_person_email.html', {
        'user_name': collect_person.order.user.username,
        'order_id':collect_person.order.order_id,
        'collect_person_name': collect_person.collect_person_name,
        'contact_number': collect_person.contact,
        'collect_date': collect_person.collect_Date,
    })
    from_email = 'onlineorders@suwaidillc.ae'  # Replace with your email

    send_mail(subject, message, from_email, [user_email], html_message=message)

@login_required
def delivery_person_asign(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            number = data.get('number')
            # inspection_date = data.get('date')
            order_id = data.get('order_id')
            print(order_id)

            # Try to get the existing record and update it or create a new one
            order_instance = Order.objects.get(order_id=order_id)
            # delivery_person, created = OrderDeliveryPerson.objects.update_or_create(
            #     order=order_instance,
            #     defaults={
            #         'delivery_person_name': name,
            #         'contact': number,
            #     }
            # )

            # Send email to the user
            # send_user_notification_email(delivery_person.order.user.email, delivery_person)


            return JsonResponse({'message': 'Data saved successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'message': f'Order with order_id {order_id} does not exist'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

@login_required
def collect_person_asign(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            number = data.get('number')
            inspection_date = data.get('date')
            order_id = data.get('order_id')
            print(order_id)

            # Try to get the existing record and update it or create a new one
            # order_instance = Order.objects.get(order_id=order_id)
            # collect_person, created = ReplacementCollectPerson.objects.update_or_create(
            #     order=order_instance,
            #     defaults={
            #         'collect_person_name': name,
            #         'contact': number,
            #         'collect_Date': inspection_date
            #     }
            # )

            # Send email to the user
            # send_user_notification_email(collect_person.order.user.email, collect_person)


            subject = 'Replacement Product Collect Person Assignment'
            # message = render_to_string('collect_person_email.html', {
            #     'user_name': collect_person.order.user.username,
            #     'order_id':collect_person.order.order_id,
            #     'collect_person_name': collect_person.collect_person_name,
            #     'contact_number': collect_person.contact,
            #     'collect_date': collect_person.collect_Date,
            # })
            # from_email = 'onlineorders@suwaidillc.ae'  # Replace with your email

            # user_email = collect_person.order.user.email
            # print(user_email)

            # send_mail(subject, message, from_email, [user_email], html_message=message)


            return JsonResponse({'message': 'Data saved successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'message': f'Order with order_id {order_id} does not exist'})
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'})
    else:
        return JsonResponse({'message': 'Invalid request method'})





# def order_status_update(request):

#     if request.method == 'POST':
#         data = json.loads(request.body)
#         order_status_update = data.get('order_status')
#         print(order_status_update)



#     return JsonResponse({'message':'status update sucessfully'})

@login_required
def send_not_approved_email(order, Comment):
    email_subject = ''
    email_body = None
    to_email = [Order.user.email]  # Default to user's email

    email_subject = 'Order Cancel Not Approved By Admin'
    email_body = render_to_string('order_cancel_notapproved_email.html', {
        'order': order,
        'user': Order.user ,
        'order_id': Order.order_id,
        'reason': Comment,
        # Include other necessary variables for the email body
    })

    if email_subject and email_body:
        safe_email_body = mark_safe(email_body)
        email = EmailMultiAlternatives(
            email_subject,
            body=safe_email_body,
            from_email='onlineorders@suwaidillc.ae',
            to=to_email,
        )
        email.attach_alternative(safe_email_body, "text/html")
        email.send()
        print(f"Email sent for Order {Order.order_id} with status {Order.cancel_status}")


@login_required
def order_status_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_status = data.get('order_status')
        print(order_status)
        order_id = data.get('order_id')
        print(order_id)
        cancel_status = data.get('cancel_status')
        print(cancel_status)
        Comment = data.get('Comment')
        print(Comment)

        

        # Retrieve the corresponding Status instance
        # try:
        #     order_status_instance = Status.objects.get(status=order_status)
        #     print(order_status_instance)
        # except Status.DoesNotExist:
        #     return JsonResponse({'error': f'Status "{order_status}" does not exist'})

        # Assuming you have an order object that you want to update
        order = Order.objects.get(order_id=order_id)  


        # Update the order status
        if order_status =='Cancelled':
            print('order status is Cancelled')
            order.cancel_status = cancel_status
            order.save()

            # Check if the cancel_status is 'NotApproved', then send the email
            if cancel_status.lower() == 'notapproved':
                send_not_approved_email(order, Comment)

        else:
            pass
            # order.order_status = order_status_instance
            # order.save()

        


        # Return a response, e.g., a success message or updated order details
        response_data = {'message': 'Order status updated successfully', 'order_status': order_status}
        return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest('Invalid request method')


# def back_order(request):

#     user = User.objects.all()
#     addresses = address.objects.filter(user__in=user, address_2=True, address_type='Billing')

#     context = {

#         'user':user,
#         'addresses':addresses,
#     }

#     return render(request, 'Al-admin/order/back_order.html', context)

@login_required
def back_order_user(request):

    user = get_user_model().objects.all()
    print(user)
    addresses = Address.objects.filter(user__in=user, address_2=True, address_type='Billing')

    context = {

        'user':user,
        'addresses':addresses,
    }

    return render(request, 'Al-admin/order/back_order.html', context)


@login_required
def back_order_form(request, id):

    user = id

    print(user)

    billing_info_details = list(Address.objects.filter(user=user, address_type='Billing').values('id', 'user', 'first_name', 'email', 'phone', 'address_1', 'address_2', 'city', 'postcode', 'Country_Region', 'address_type'))
    print('billing_info_details', billing_info_details)

    shipping_info_details = Address.objects.filter(user=user, address_type='Shipping').values()
    print('shipping_info_details', shipping_info_details)

    products_list =Product.objects.all()
    # Number of items to display per page
    items_per_page = 30

    # Create a Paginator object
    paginator = Paginator(products_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the products for the current page
        products_page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, deliver the last page of results.
        products_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products_page = paginator.page(1)
    
    Categorys = ParentCategory.objects.all()
    subCategories = SubCategory.objects.all()
    brand = Brand.objects.all()
    attribute = Attribute.objects.all()


    billingaddress = json.dumps(list(billing_info_details))

    context = {

        'product': products_page,
        'Categorys':Categorys,
        'subCategories':subCategories,
        'brand':brand,
        'attribute':attribute,
        'billing_info_details':billing_info_details,
        'shipping_info_details':shipping_info_details,
        'user':user,
    }

    return render(request, 'Al-admin/order/back-order-creation-form.html', context)


@login_required
def order_product_selection(request):
     if request.method == 'POST':
        data = json.loads(request.body)
        selected_values = data.get('selectedValues')
        # Get the count of selected values
        count = len(selected_values)
        print("Selected values count", count)

        product_data = []  # Create an empty list to store the results

        sub_total = 0

        row_total = 0

        disc_total = 0

        for item in selected_values:
            id_value = item.get('id')
            quantity = item.get('quantity')
        
            order_product = Product.objects.values('pk','name', 'sku',  'regular_price', 'sale_price').filter(id__in=id_value)

            # Create a dictionary for each product and include quantity
            for product in order_product:
                price = product['regular_price']
                print(price)
                print(type(quantity))
                special_price = product['sale_price']
                # Check if special_price is None and treat it as 0
                if special_price is None:
                    special_price = 0

                    # Use a conditional expression to set 'Discount' value
                    discount = special_price if special_price is not None else 0
                    
                

                subtotal = int(quantity) * price
                print(subtotal)

                sub_total += subtotal

                disc_total += special_price

                row_total_price = subtotal + special_price

                row_total += row_total_price

                product_data.append({
                    'pk': product['pk'],
                    'product_name': product['name'],
                    'product_sku': product['sku'],
                    # 'product_Image1': product['product_Image1'],
                    'price': product['regular_price'],
                    'quantity': quantity,
                    'subtotal':subtotal,
                    'Discount':discount,
                    'row_total_price': row_total_price,
                    
                })
            print(product_data)
            print("sub_total", sub_total)
            print("disc_total", disc_total)
            print("row_total", row_total)

            data = {
                'product_data':list(product_data),
                'sub_total':sub_total,
                'disc_total':disc_total,
                'row_total':row_total,
                'count':count,
            }

        return JsonResponse(data, safe=False)
     



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@csrf_exempt
def back_order(request, product_id=None):
    print(product_id)

    if request.method == 'POST':

        
        data = json.loads(request.body)
        user_id =data.get('userId')
        print(user_id)
        user = get_user_model().objects.get(pk=user_id)
        print(user)
        cart_items = data.get('cartItems')
        print(cart_items)
        shipping_info = data.get('shipping_info')
        print('shipping_info', shipping_info)
        billing_info = data.get('billing_info')
        print(type(billing_info))
        print('billing_info', billing_info)
        total_amount = data.get('total_amount')
        


        # tax = Tax.objects.get(Active = True)

        # tax_amount =  int(total_amount)*int(tax.tax_valu)/100
        # print('tax ammount')
        # print(tax_amount)

        # amount = int(int(total_amount) - float(tax_amount))
        # print("total amount")
        # print(amount)

        shipping_cost = data.get('shipping_cost')
        print(shipping_cost)

        discount = data.get('discount')
        print(discount)

        payment = 'Cash On Delivery'
        print(payment)

        coupon_code = data.get('coupon_code')
        print("coupon code value")
        print(coupon_code)

        
        email_confirm = data.get('email_confirm')
        print('email_confirm', email_confirm)

        Commentscheckbox = data.get('Commentscheckbox')
        print('Commentscheckbox', Commentscheckbox)

        Comments = data.get('Comments')
        print('Comments', Comments)

        order_date = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        print(order_date)

        for item in cart_items:
            product_id = item.get('id')
            print(product_id)
            quantity = item.get('quantity')
            print('quantity value')
            print(quantity)
            product = Product.objects.get(id=product_id)
            print(product)
            name = product.name
            print(name)
            total = item.get('total_amount')
            print(total)

            product_quantity = Product.objects.get(id=product_id)
            print('products quantity checking')
            print(product_quantity.stock)

            if int(quantity) <= int(product_quantity.stock):

                print("quantity available")

                # Check if billing_info is an integer (existing address ID)
                if isinstance(billing_info, int):
                    print('isinstance work')
                    billing_address = Address.objects.get(id=billing_info)
                else:
                    # Create a new billing address
                    billing_address = Address.objects.create(
                        user=user,
                        name=billing_info['first_name'],
                        email=billing_info['email'],
                        phone=billing_info['phone'],
                        address_1=billing_info['address_1'],
                        address_2=billing_info['address_2'],
                        # landmark=billing_info['landmark'],
                        city=billing_info['city'],
                        state=billing_info[' state_country'],
                        postcode=billing_info['postcode'],
                        Country_Region =billing_info['Country_Region'],
                        address_type = 'Billing',
                        Active = True,
                    )
                print(billing_address)

                # Check if shipping_info is an integer (existing address ID)
                if isinstance(shipping_info, int):
                    shipping_address = Address.objects.get(id=shipping_info)
                else:
                    # Create a new billing address
                    shipping_address = Address.objects.create(
                        user=user,
                        name=shipping_info['first_name'],
                        email=shipping_info['email'],
                        phone=shipping_info['phone'],
                        address_1=billing_info['address_1'],
                        address_2=billing_info['address_2'],
                        city=shipping_info['city'],
                        state=shipping_info[' state_country'],
                        postcode=shipping_info['postcode'],
                        Country_Region =shipping_info['Country_Region '],
                        address_type = 'Shipping',
                        Active = True,
                    )
                print(shipping_address)

                order = Order.objects.create(
                    user=user,
                    Billing_address_id=billing_info,
                    shipping_address_id=shipping_info,
                    # amount=amount,
                    disc_price=discount,
                    # tax_amount = tax_amount,
                    bill_amount=total_amount,
                    shipping_cost=shipping_cost,
                    payment_method_id=1,
                    order_status_id=2,

               )
                print("order store")

                # Retrieve the order_id
                order_id = order.order_id

                for item in cart_items:
                    product_id = item.get('id')
                    print(product_id)
                    quantity = item.get('quantity')
                    print('quantity value')
                    print(quantity)
                    product = Product.objects.get(id=product_id)
                    print(product)
                    name = product.name
                    print(name)
                    total = item.get('subtotal')
                    print(total)


                    order_item = OrderItem.objects.create(

                    order_id=order,
                    product_id=product,
                    product_name=name,
                    price=product.regular_price,
                    quentity=quantity,
                    # disc_price=0,
                    total=total
                    )
                    print("order iteam also store")

                

                if coupon_code is not None and coupon_code != '':
                    try:
                        coupon_val = Coupon.objects.get(code=coupon_code)
                        CouponUsage.objects.get_or_create(coupon=coupon_val, user=request.user)
                        print('Coupon applied successfully and stored in CouponUsage')
                    except ObjectDoesNotExist:
                        print('Coupon does not exist')  # Handle the case where the coupon does not exist


                 # After the order is created
                invoice_id = f"{order_id}-INV"
                invoice_date = date.today()
                invoice = Invoice.objects.create(
                    invoice_id=invoice_id,
                    invoice_date=invoice_date,
                    user=user,
                    order=order,
                )
                print("invoice created")
                print(order.order_id)

                if email_confirm == True:


                    item_count = OrderItem.objects.filter(order_id=order.id).count()
                    print(item_count)

                    # Send confirmation email
                    email_subject = 'Your Alsuwaidi in  Order #{} of {} item'.format(order.order_id, item_count) 

                    # current_site = get_current_site(request)
                    # site_url = f"https://{current_site.domain}"
                    # print(site_url)
                    
                    track_url = reverse('order_tracking', kwargs={'order_id': order_id})
                    invoice_url = reverse('download_invoice', kwargs={'order_id': order.id, 'invoice_id': invoice_id})

                    # order_track = f"{site_url}{track_url}"
                    # order_invoice = f"{site_url}{invoice_url}"

                    # print(order_track)
                    # print(order_invoice)

                    print(order_item )

                    if Commentscheckbox == True:
                        email_Comments = Comments

                    email_body = render_to_string('order_confirmation_email.html', {
                        'order': order,
                        'order_item':OrderItem.objects.filter(order_id=order.id),
                        'user': user,
                        'order_id': order_item.order_id,
                        'shippingaddress': Address.objects.get(id=order.shipping_address_id),
                        'billingaddress': Address.objects.get(id=order.Billing_address_id),
                        # 'payment': payment_method.objects.values_list('payment_name', flat=True).get(id=order.payment_method_id),
                        'iteam_total': order.amount,
                        'tax':order.tax_amount,
                        'disc_price':order.disc_price,
                        'total':order.bill_amount,
                        # 'product_details': products.objects.filter(product_name=order_item.product_id),
                        'order_date':order.order_date,
                        # 'site_url':site_url,
                        # 'order_track':order_track,
                        # 'order_invoice':order_invoice,
                        'email_Comments':email_Comments,
                        
                    })   
                    safe_email_body = mark_safe(email_body)
                    email = EmailMultiAlternatives(
                    email_subject, 
                    body=safe_email_body, 
                    from_email='onlineorders@suwaidillc.ae', 
                    to=[user.email],
                    )   
                    email.attach_alternative(safe_email_body, "text/html")


                    # Send email to admin
                    admin_email = settings.ADMIN_EMAIL
                    cc_email = settings.CC_EMAIL
                    # admin_subject = 'New Order Received'
                    admin_subject = f"New order received from {user.username}. Order ID: {order.order_id}"
                    
                    admin_email_body = render_to_string('admin_order_notification_email.html', {
                        'order': order,
                        'order_item':OrderItem.objects.filter(order_id=order.id),
                        'user': user,
                        'order_id': order_item.order_id,
                        'shippingaddress': Address.objects.get(id=order.shipping_address_id),
                        'billingaddress': Address.objects.get(id=order.Billing_address_id),
                        # 'payment': payment_method.objects.values_list('payment_name', flat=True).get(id=order.payment_method_id),
                        'iteam_total': order.amount,
                        'tax':order.tax_amount,
                        'disc_price':order.disc_price,
                        'total':order.bill_amount,
                        # 'product_details': products.objects.filter(product_name=order_item.product_id),
                        'order_date':order.order_date,
                        # 'site_url':site_url,
                        # 'order_track':order_track,
                        # 'order_invoice':order_invoice,
                    })
                    safe_admin_email_body = mark_safe(admin_email_body)
                    admin_email = EmailMultiAlternatives(
                        admin_subject,
                        safe_admin_email_body,
                        from_email='onlineorders@suwaidillc.ae',
                        to=[admin_email],
                        cc=cc_email,
                    )
                    admin_email.attach_alternative(safe_admin_email_body, "text/html")
                    admin_email.send()


                    email.send()
                    print("email send to user and Admin")
                
                data = {
                    'success': True,
                    # 'order_id':order_id,
                }
                print(data)
                return JsonResponse(data, safe=False)

            else:
                print("quantity not available")
                response_data = {'success': False}
                return JsonResponse(response_data)
    else:
        print("Post function is not work ")
        response_data = {
            'success': False,
        }
        return JsonResponse(response_data)
    

@login_required
def Dashboard(request):
    # order_status = Status.objects.all()
    orders = Order.objects.all().order_by('-order_date').values('user__username', 'amount', 'order_id', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date')
    print(orders)

    # Query the database to get monthly sales counts
    # order_data = Order.objects.annotate(
    #     month=TruncMonth('order_date')
    # ).values('month').annotate(count=Count('id')).order_by('month')

    # Calculate the date 7 days ago from today
    seven_days_ago = timezone.now() - timedelta(days=7)

    # Filter orders within the last 7 days
    order_data = Order.objects.filter(order_date__gte=seven_days_ago.date())


    order_data = Order.objects.annotate(
        day=TruncDate('order_date')
    ).values('day').annotate(count=Count('id')).order_by('day')

    # Extract month labels and sales counts
    labels = [entry['day'].strftime('%b %d, %Y') for entry in order_data]
    order_counts = [entry['count'] for entry in order_data]

    chart_data = {
        'labels': labels,
        'order_counts': order_counts,
    }

    # Filter orders within the last 7 days
    daily_sales = Order.objects.filter(order_date__gte=seven_days_ago.date())

    daily_sales = Order.objects.annotate(order_day=TruncDate('order_date')).values('order_day').annotate(total_sales=Sum('bill_amount')).order_by('order_day')
    print('daily_sales')
    print(daily_sales)
    # Extract daily labels and sales counts
    daily_labels = [entry['order_day'].strftime('%b %d, %Y') for entry in daily_sales]
    print(daily_labels)
    daily_sales_counts = [entry['total_sales'] for entry in daily_sales]
    print(daily_sales_counts)

    daily_sales_data = {
        'labels': daily_labels,
        'daily_sales_counts': daily_sales_counts,
    }

    total_order = Order.objects.all().count()
    print(total_order)

    new_order = Order.objects.filter(order_status = 'Confirmed').count()
    print(new_order)

    order_process = Order.objects.filter(order_status = 'Shipped').count()
    print(order_process)

    order_delivered = Order.objects.filter(order_status = 'Delivered').count()
    print(order_delivered)


    order_replacement = Order.objects.filter(order_status = 'Replacement').count()
    print(order_replacement)


    all_Time_total =Order.objects.aggregate(total=Sum('bill_amount'))['total']
    print(all_Time_total)

    # Check if there are any orders in the database
    if all_Time_total is None:
        all_Time_total = 0


    # Get the current date
    today = timezone.now().date()

    # Use the aggregate function to calculate the sum of bill_amount for today's orders
    today_total = Order.objects.filter(order_date=today).aggregate(total=Sum('bill_amount'))['total']
    print(today_total)


    # Calculate total amount for Cash on Delivery orders
    day_cash_on_delivery_total = Order.objects.filter(
        order_date=today,
        payment_method='Cash On Delivery'  # Replace with the actual method name
    ).aggregate(total=Sum('bill_amount'))['total']

    # Calculate total amount for Payment orders
    day_payment_total = Order.objects.filter(
        order_date=today,
        payment_method='Online Payment'  # Replace with the actual method name
    ).aggregate(total=Sum('bill_amount'))['total']

    print("Cash on Delivery Total:", day_cash_on_delivery_total)
    print("Payment Total:", day_payment_total)


    # Check if there are any orders for today
    if today_total is None:
        today_total = 0

    # Check if there are any orders for today
    if day_cash_on_delivery_total is None:
        day_cash_on_delivery_total = 0

    # Check if there are any orders for today
    if day_payment_total is None:
        day_payment_total = 0


    # Calculate the start date for the past week (7 days ago)
    one_week_ago = today - timedelta(days=7)

    # Calculate the total amount for orders placed within the past week
    weekly_total = Order.objects.filter(
        order_date__range=[one_week_ago, today]
    ).aggregate(total=Sum('bill_amount'))['total']

    # Calculate total amount for Cash on Delivery orders
    week_cash_on_delivery_total = Order.objects.filter(
        order_date__range=[one_week_ago, today],
        payment_method='Cash On Delivery'  # Replace with the actual method name
    ).aggregate(total=Sum('bill_amount'))['total']

    # Calculate total amount for Payment orders
    week_payment_total = Order.objects.filter(
        order_date__range=[one_week_ago, today],
        payment_method='Online Payment'  # Replace with the actual method name
    ).aggregate(total=Sum('bill_amount'))['total']

    print("week Cash on Delivery Total:", week_cash_on_delivery_total)
    print("week Payment Total:", week_payment_total)

    print("Weekly Total Amount:", weekly_total)


    # Check if there are any orders for today
    if weekly_total is None:
        weekly_total = 0

    # Check if there are any orders for today
    if week_cash_on_delivery_total is None:
        week_cash_on_delivery_total = 0

    # Check if there are any orders for today
    if week_payment_total is None:
        week_payment_total = 0


    # Calculate the start date of the current month
    first_day_of_month = today.replace(day=1)

    # Use the aggregate function to calculate the sum of bill_amount for this month's orders
    month_total = Order.objects.filter(order_date__gte=first_day_of_month).aggregate(total=Sum('bill_amount'))['total']

    # Check if there are any orders for this month
    if month_total is None:
        month_total = 0


    # outof_stock = products.objects.filter(in_stock = 'Out of Stock').count()


    best_selling_product = Product.objects.filter(stock=0).order_by('-stock')[:12]  # Retrieve the product with the highest sales count
    print(best_selling_product)

    # top_viewed_products = (ViewedProduct.objects.values('product').annotate(view_count=Count('product')).order_by('-view_count').values('product__product_name', 'product__product_sku', 'product__price', 'view_count')[:12] )
    # print(top_viewed_products)

    two_days_ago = today - timedelta(days=2)

    new_users_data = get_user_model().objects.filter(
        date_joined__date__gte=seven_days_ago.date()
        ).annotate(
            order_count=Count('Order'),
            total_order_amount=Sum('Order__bill_amount')
        ).values('user_nicename', 'email')

    print(new_users_data)

    all_users_data = get_user_model().objects.all().annotate(
            order_count=Count('Order'),
            total_order_amount=Sum('Order__bill_amount')
        ).values('user_nicename', 'email')

    print(all_users_data)

    context = {
        'total_order':total_order,
        'new_order':new_order,
        'order_process':order_process,
        'order_delivered':order_delivered,
        'order_replacement':order_replacement,
        # 'order_status':order_status,
        'orders':orders,
        'chart_data':chart_data,
        'daily_sales_data':daily_sales_data,
        'all_Time_total':all_Time_total,
        'today_total':today_total,
        'day_cash_on_delivery_total':day_cash_on_delivery_total,
        'day_payment_total':day_payment_total,
        'weekly_total':weekly_total,
        'week_cash_on_delivery_total':week_cash_on_delivery_total,
        'week_payment_total':week_payment_total,
        'month_total':month_total,
        'best_selling_product':best_selling_product,
        # 'top_viewed_products':top_viewed_products,
        # 'new_users_data':new_users_data,
        # 'all_users_data':all_users_data,
    }
    return render(request, 'Al-admin/Dashboard/dashboard.html', context)

@login_required
def order_data_get(request, category=None):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        order_data = data.get('order_data')
        print(order_data)
        
        data = {
            'order_data':order_data,
        }

        return JsonResponse(data)

        # order = Order.objects.filter(order_status = order_data)
        # print(order)

    order = Order.objects.filter(Q(order_status=category) | Q(payment_status=category)).order_by('-order_date').values('user__username', 'amount', 'disc_price', 'tax_amount', 'shipping_cost',  'order_id', 'billing_address', 'shipping_address', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date')
    print(order)

    order_count = Order.objects.all().order_by('-order_date')

    all_order_count = order_count.count()
    print(all_order_count)
    payment_Pending_count = order_count.filter(payment_status='Pending').count()
    print(payment_Pending_count)
    order_delivered_count = order_count.filter(order_status='Delivered').count()
    print(order_delivered_count)
    order_cancelled_count = order_count.filter(order_status='Cancelled').count()
    print(order_cancelled_count)
    order_shipped_count = order_count.filter(order_status='Shipped').count()
    print(order_shipped_count)
    # order_status = Status.objects.all()
    # print(order_status)
    # payment_type = payment_method.objects.all()
    # print(payment_type)


    context = {
        'order':order,
        'all_order_count':all_order_count,
        'payment_Pending_count':payment_Pending_count,
        'order_delivered_count':order_delivered_count,
        'order_cancelled_count':order_cancelled_count,
        'order_shipped_count':order_shipped_count,
        # 'order_status':order_status,
        # 'payment_type':payment_type,
    }
    return render(request, 'Al-admin/order/order.html', context)

    
@login_required
def product_data_get(request, category=None):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        order_data = data.get('order_data')
        print(order_data)
        
        data = {
            'order_data':order_data,
        }

        return JsonResponse(data)
    
    
    status = 'Out of Stock'

    products_list = Product.objects.filter(in_stock = status)
    all_count = Product.objects.all().count()
    publish_count = Product.objects.filter(published = True).count()
    unpublish_count = Product.objects.filter(published = False).count()

    outofstock_count =Product.objects.filter(in_stock = 'Out of Stock').count()
    categories = ParentCategory.objects.all()
    subCategories = SubCategory.objects.all()
    brand = Brand.objects.all()

    # Number of items to display per page
    items_per_page = 30

    # Create a Paginator object
    paginator = Paginator(products_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the products for the current page
        products_page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, deliver the last page of results.
        products_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products_page = paginator.page(1)

    context = {
        'product': products_page,
        'categories': categories,
        'subCategories': subCategories,
        'brand': brand,
        'all_count':all_count,
        'publish_count':publish_count,
        'unpublish_count':unpublish_count,
        'outofstock_count':outofstock_count,
    }
    
    return render(request, "Al-admin/product/product_admin.html", context)

@login_required
def product_filter_data(request, category=None):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        order_data = data.get('order_data')
        print(order_data)
        
        data = {
            'order_data':order_data,
        }

        return JsonResponse(data)
    
    products_list = Product.objects.filter(published  = category)
    print(products_list)
    all_count = Product.objects.all().count()
    publish_count = Product.objects.filter(published = True).count()
    unpublish_count = Product.objects.filter(published = False).count()
    outofstock_count = Product.objects.filter(in_stock = 'Out of Stock').count()
    categories = ParentCategory.objects.all()
    subCategories =SubCategory.objects.all()
    brand = Brand.objects.all()

    # Number of items to display per page
    items_per_page = 30

    # Create a Paginator object
    paginator = Paginator(products_list, items_per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the products for the current page
        products_page = paginator.page(page_number)
    except EmptyPage:
        # If the requested page is out of range, deliver the last page of results.
        products_page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products_page = paginator.page(1)

    context = {
        'product': products_page,
        'categories': categories,
        'subCategories': subCategories,
        'brand': brand,
        'all_count':all_count,
        'publish_count':publish_count,
        'unpublish_count':unpublish_count,
        'outofstock_count':outofstock_count,
    }
    
    return render(request, "Al-admin/product/product_admin.html", context)




# def customer(request):
#     # customer = User.objects.all().values()

#     customers = get_user_model().objects.annotate(
#         total_orders=Count('Order'),  # Calculate the total order count
#         total_spent=Sum('Order__bill_amount'),  # Calculate the total money spent
#         last_order_date=Max('Order__order_date')  # Find the last order date
#     )

#      # Retrieve the default billing address city for each user
#     for customer in customers:
#         default_billing_address = address.objects.filter(
#             user=customer,
#             address_type='Billing',
#             address_2=True
#         ).first()

#         if default_billing_address:
#             customer.billing_city = default_billing_address.city
#         else:
#             customer.billing_city = None

#     print(customers)



#     context = {
#         'customers':customers,
#     }
#     return render(request, 'Al-admin/customer/customer.html', context)


class CustomerListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'Al-admin/customer/customer.html'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            total_orders=Count('Order'),
            total_spent=Sum('Order__bill_amount'),
            last_order_date=Max('Order__order_date')
        )

        for customer in queryset:
            default_billing_address = Address.objects.filter(
                user=customer,
                address_type='Billing',
                address_2=True
            ).first()

            if default_billing_address:
                customer.billing_city = default_billing_address.city
            else:
                customer.billing_city = None

        return queryset
    
    def dispatch(self, request, *args, **kwargs):
        user_has_permission = request.user.has_perm('user.view_user')

        # Check group permissions if user does not have direct permission
        if not user_has_permission:
            user_groups = request.user.groups.all()
            for group in user_groups:
                if group.permissions.filter(codename='view_user').exists():
                    user_has_permission = True
                    break

        if not user_has_permission:
            # Return some error or handle permission denial
            return render(request, 'Al-admin/permission/permission_denied.html')

        return super().dispatch(request, *args, **kwargs)


@login_required
def customer_details(request, id):
    print(id)

    user = get_user_model().objects.get(id=id)
    print(user)

    # order Get user based
    order = Order.objects.filter(user = id).order_by('-order_date').values('order_id', 'bill_amount', 'order_status', 'payment_status' , 'payment_method', 'order_date')
    print(order)

    order_count = order.count()
    #wishlist get user based
    wish_list = WishlistItem.objects.filter(user=id)
    print(wish_list)

    wishlist_count = wish_list.count()

    rating_review = Rating.objects.filter(user=id)
    print(rating_review)

    rate_count = rating_review.count()

    def_address = None
    try:
        def_address = Address.objects.values().get(user=id, address_type='Billing', address_2=True)
        print('def_address')
        print(def_address)
    except Address.DoesNotExist:
        print("No default billing address found.")

    context = {
        'order':order,
        'wish_list':wish_list,
        'order_count':order_count,
        'wishlist_count':wishlist_count,
        'rating_review':rating_review,
        'rate_count':rate_count,
        'user':user,
        'def_address':def_address,
    }

    return render(request, 'Al-admin/customer/customer_details.html', context)


@login_required
def delete_customer(request, customerId):
    if request.method == 'POST':
        try:
            Customer = get_user_model().objects.get(id=customerId)
            print(Customer)
            Customer.delete()
            return JsonResponse({'message': 'Customer deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Customer not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)


@login_required
def coupon(request):
    Coupons = Coupon.objects.all()
    print(Coupons)

    user_has_permission = request.user.has_perm('products.view_coupon')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_coupon').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'Coupons':Coupons,
    }
    return render(request, 'Al-admin/Coupon/Coupon.html', context)

@login_required
def addcoupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon')
        print(code)
        discount = request.POST.get('discount_type')
        print(discount)
        valid_from_str = request.POST.get('coupon_start_date')
        print(valid_from_str)
        valid_to_str = request.POST.get('coupon_end_date')
        print(valid_to_str)
        active = request.POST.get('active')
        print(active)
        

        try:
            # Parse the date and time strings into datetime objects
            valid_from = datetime.strptime(valid_from_str, '%d/%m/%y %H:%M')
            valid_to = datetime.strptime(valid_to_str, '%d/%m/%y %H:%M')

            if active =='on':
                Active = True
            else:
                Active = False

            # Create a new Coupon instance and save it
            coupon = Coupon(code=code, discount=discount, valid_from=valid_from, valid_to=valid_to, Active=Active)
            coupon.save()

            return JsonResponse({'message': 'Coupon added successfully'})
        except ValueError:
            return JsonResponse({'error': 'Invalid date or time format'})

    return JsonResponse({'error': 'Invalid request method'})

@login_required
def couponUseage(request):
    coupon_useage = CouponUsage.objects.all()
    print(coupon_useage)

    user_has_permission = request.user.has_perm('checkout.view_couponusage')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_couponusage').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'coupon_useage':coupon_useage,
    }
    return render(request, 'Al-admin/Coupon/Couponuseage.html', context)

@login_required
def update_coupon(request):
    if request.method == 'POST':
        print('coupon update form post a value')
        coupon_id = request.POST.get('coupon_id')
        print(coupon_id)
        code = request.POST.get('coupon')
        print(code)
        discount = request.POST.get('discount_type')
        print(discount)
        valid_from_str = request.POST.get('coupon_start_date')
        print(valid_from_str)
        valid_to_str = request.POST.get('coupon_end_date')
        print(valid_to_str)
        active = request.POST.get('active')
        print(active)

        
        try:

            # Fetch the existing coupon
            coupon = Coupon.objects.get(id=coupon_id)
            print(coupon)

            # Parse the date and time strings into datetime objects
            valid_from = datetime.strptime(valid_from_str, '%d/%m/%y %H:%M')
            valid_to = datetime.strptime(valid_to_str, '%d/%m/%y %H:%M')

            if active =='on':
                Active = True
            else:
                Active = False

            # Update the coupon fields
            coupon.coupon = code
            coupon.discount_type = discount
            coupon.coupon_start_date = valid_from
            coupon.coupon_end_date = valid_to
            # coupon.Active = Active
            coupon.save()

            return JsonResponse({'message': 'Coupon added successfully'})
        except ValueError:
            return JsonResponse({'error': 'Invalid date or time format'})

        # Return a JSON response indicating success or failure
        return JsonResponse({'message': 'Coupon updated successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def delete_coupon(request, coupon_id):
    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            print(coupon)
            coupon.delete()
            return JsonResponse({'message': 'Coupon deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Coupon not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def export_out_of_stock_to_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="out_of_stock_products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Product SKU', 'Stock In Quantity'])

    out_of_stock_products = Product.objects.filter(in_stock='Out of Stock')

    for product in out_of_stock_products:
        writer.writerow([
            product.sku,
            product.stock
        ])

    return response

@login_required
def import_stock_from_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            # Assuming the CSV file has headers
            headers = next(csv_reader)
            sku_index = headers.index('Product SKU')
            stock_in_index = headers.index('Stock In Quantity')

            for row in csv_reader:
                sku = row[sku_index]
                stock_in_quantity = int(row[stock_in_index])

                try:
                    product = Product.objects.get(product_sku=sku)
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with SKU {sku} not found'})

                product.stock = stock_in_quantity
                
                if stock_in_quantity == 0:
                    product.in_stock = 'Out of Stock'
                else:
                    product.in_stock = 'Instock'

                product.save()

            # Redirect to product-admin page after a successful import
            return JsonResponse({"success": "Products Stock imported successfully."})

        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"})

    return render(request, 'Al-admin/product/import_stock.html')


# @login_required
# def import_attribute_from_csv(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']

#         try:
#             decoded_file = csv_file.read().decode('utf-8').splitlines()
#             csv_reader = csv.reader(decoded_file)

#             # Assuming the CSV file has headers
#             headers = next(csv_reader)
#             sku_index = headers.index('Product_Sku')
#             sub_category_index = headers.index('Sub_Category')
#             attribute_index = headers.index('Attribute')
#             attribute_value_index = headers.index('Attribute_Value')

#             for row in csv_reader:
#                 # Check if Attribute exists or create new
#                 attribute_name = row[attribute_index]
#                 attribute, created = Attribute.objects.get_or_create(name=attribute_name)
                
#                 # Check if AttributeValue exists or create new
#                 attribute_value_name = row[attribute_value_index]
#                 attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_value_name, Active=True)

#                 # Check if subCategory exists or create new
#                 subcategory_name = row[sub_category_index]
#                 subcategory, created = subCategory.objects.get_or_create(name=subcategory_name)

#                 # Check if Category_attribute_map exists or create new
#                 category_attribute_map, created = Category_attribute_map.objects.get_or_create(
#                     subCategory=subcategory,
#                     attribute=attribute,
#                     # Slot_Position=row['category_slot_position'],
#                     Active=True
#                 )

#                 # Retrieve product ID based on product SKU
#                 product_sku = row[sku_index]
#                 product = products.objects.get(product_sku=product_sku)

#                 # Check if product_attr_values_map exists or create new
#                 product_attr_value_map, created = product_attr_values_map.objects.get_or_create(
#                     product=product,
#                     subcategory=subcategory,
#                     attribute=attribute,
#                     attribute_value=attribute_value,
#                     Active=True
#                 )

#                 print(product_attr_value_map)

#             return JsonResponse({'success':'Attribute Updated Sucessfully'})

#         except Exception as e:
#             return JsonResponse({'error': f'Error: {str(e)}'})

#     return render(request, 'Al-admin/product/import_attribute.html')



@login_required
def import_attribute_from_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)

            # Assuming the CSV file has headers
            headers = next(csv_reader)
            sku_index = headers.index('Product_Sku')
            sub_category_index = headers.index('Sub_Category')
            attribute_index = headers.index('Attribute')
            attribute_value_index = headers.index('Attribute_Value')

            for row in csv_reader:
                # Retrieve product ID based on product SKU
                product_sku = row[sku_index]
                product = Product.objects.get(product_sku=product_sku)

                # Check if subCategory exists or create new
                subcategory_name = row[sub_category_index]
                subcategory, created = SubCategory.objects.get_or_create(name=subcategory_name)

                # Split attribute and attribute value pairs
                attributes = row[attribute_index].split(',')  # Assuming attributes are separated by comma
                attribute_values = row[attribute_value_index].split(',')  # Assuming attribute values are separated by comma

                # Iterate over each attribute and attribute value pair
                for attribute_name, attribute_value_name in zip(attributes, attribute_values):
                    # Check if Attribute exists or create new
                    attribute, created = Attribute.objects.get_or_create(name=attribute_name)
                    
                    # Check if AttributeValue exists or create new
                    attribute_value, created = AttributeValue.objects.get_or_create(attribute=attribute, value=attribute_value_name, Active=True)

                    # Check if Category_attribute_map exists or create new
                    # category_attribute_map, created = Category_attribute_map.objects.get_or_create(
                    #     subCategory=subcategory,
                    #     attribute=attribute,
                    #     Active=True
                    # )

                    # Check if product_attr_values_map exists or create new
                    # product_attr_value_map, created = product_attr_values_map.objects.get_or_create(
                    #     product=product,
                    #     subcategory=subcategory,
                    #     attribute=attribute,
                    #     attribute_value=attribute_value,
                    #     Active=True
                    # )

                    # print(product_attr_value_map)

            # return JsonResponse({'success':'Attribute Updated Sucessfully'})
            return redirect('attribute-admin')

        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'})

    return render(request, 'Al-admin/product/import_attribute.html')



@login_required
def export_attribute_values(request):
    response = AttributeValue.export_to_csv()
    return response



class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'Al-admin/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')
        filter = ProductFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter

        # Custom pagination logic
        items_per_page = self.paginate_by
        paginator = Paginator(filter.qs, items_per_page)
        page_number = self.request.GET.get('page', 1)

        try:
            product = paginator.page(page_number)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)
            return HttpResponse("Page not found.")
        except PageNotAnInteger:
            product = paginator.page(1)

        current_page = product.number
        page_range = list(range(max(current_page - 2, 1), min(current_page + 3, paginator.num_pages + 1)))

        # Additional data
        all_count = Product.objects.all().count()
        publish_count = Product.objects.filter( published=True).count()
        unpublish_count = Product.objects.filter( published=False).count()
        outofstock_count = Product.objects.filter(in_stock='Out of Stock').count()

        context['products'] = product
        context['page_range'] = page_range
        context['all_count'] = all_count
        context['publish_count'] = publish_count
        context['unpublish_count'] = unpublish_count
        context['outofstock_count'] = outofstock_count


        return context
    
    def dispatch(self, request, *args, **kwargs):
        user_has_permission = request.user.has_perm('products.view_products')

        # Check group permissions if user does not have direct permission
        if not user_has_permission:
            user_groups = request.user.groups.all()
            for group in user_groups:
                if group.permissions.filter(codename='view_products').exists():
                    user_has_permission = True
                    break

        if not user_has_permission:
            # Return some error or handle permission denial
            return render(request, 'Al-admin/permission/permission_denied.html')

        return super().dispatch(request, *args, **kwargs)



# class csv_CreationListView(ListView):
#     model = csv_Creation
#     template_name = 'Al-admin/Csv/csv_admin.html'
#     context_object_name = 'csv_Creation_data'
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = csv_Creation.objects.all()
#         filter = csv_CreationFilter(self.request.GET, queryset=queryset)
#         return filter.qs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         filter = csv_CreationFilter(self.request.GET, queryset=self.get_queryset())
#         context['filter'] = filter

#         items_per_page = self.paginate_by
#         paginator = Paginator(filter.qs, items_per_page)
#         page_number = self.request.GET.get('page', 1)

#         try:
#             csv_data = paginator.page(page_number)
#         except EmptyPage:
#             csv_data = paginator.page(paginator.num_pages)
#             return HttpResponse("Page not found.")
#         except PageNotAnInteger:
#             csv_data = paginator.page(1)

#         current_page = csv_data.number
#         page_range = list(range(max(current_page - 2, 1), min(current_page + 3, paginator.num_pages + 1)))

#         context['csv_Creation_data'] = csv_data  # Ensure consistency with context object name
#         context['page_range'] = page_range

#         Badge = badge.objects.all()
#         context['Badge'] = Badge

#         return context
    


class csv_CreationListView(LoginRequiredMixin, ListView):
    # model = csv_Creation
    template_name = 'Al-admin/Csv/csv_admin.html'
    context_object_name = 'csv_Creation_data'
    paginate_by = 10

    def get_queryset(self):
        # queryset = csv_Creation.objects.all()
        # filter = csv_CreationFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = csv_CreationFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter

        items_per_page = self.paginate_by
        paginator = Paginator(filter.qs, items_per_page)
        page_number = self.request.GET.get('page', 1)

        try:
            csv_data = paginator.page(page_number)
        except EmptyPage:
            csv_data = paginator.page(paginator.num_pages)
            return HttpResponse("Page not found.")
        except PageNotAnInteger:
            csv_data = paginator.page(1)

        current_page = csv_data.number
        page_range = list(range(max(current_page - 2, 1), min(current_page + 3, paginator.num_pages + 1)))

        context['csv_Creation_data'] = csv_data  # Ensure consistency with context object name
        context['page_range'] = page_range

        # Badge = badge.objects.all()
        # context['Badge'] = Badge

        return context    

    def dispatch(self, request, *args, **kwargs):
        user_has_permission = request.user.has_perm('csvdata.view_csv_creation')

        # Check group permissions if user does not have direct permission
        if not user_has_permission:
            user_groups = request.user.groups.all()
            for group in user_groups:
                if group.permissions.filter(codename='view_csv_creation').exists():
                    user_has_permission = True
                    break

        if not user_has_permission:
            # Return some error or handle permission denial
            return render(request, 'Al-admin/permission/permission_denied.html')

        return super().dispatch(request, *args, **kwargs)



# def mainbanner (request):
#     if request.method == 'POST':
#         form = mainbanner Form(data=request.POST, files=request.FILES)        
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('Buy-Promo-Banner'))
#     else:
#         form = mainbanner Form()

#     banners = mainbanner .objects.all()
    
#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Apply search
#     if search_query:
#         banners = banners.filter(banner_url__icontains=search_query)

#     context = {
#         'banners': banners,
#         'form': form,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/banner/buy_promo_banner.html", context)

# MAIN BANNER

@login_required
def mainpage_Banner(request, banner_id=None):
    # Check if banner_id is provided, if so, get the instance of the banner
    if banner_id:
        banner_instance = get_object_or_404(MainBanner, pk=banner_id)
    else:
        banner_instance = None

    if request.method == 'POST':
        # If banner_instance exists, pass it to the form to update the existing banner
        form =mainBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Buy-Promo-Banner'))
    else:
        # If banner_instance exists, initialize the form with its instance
        form = mainBannerForm(instance=banner_instance)

    banners = MainBanner.objects.all()
    
    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Apply search
    if search_query:
        banners = banners.filter(url__icontains=search_query)


    user_has_permission = request.user.has_perm('banners.view_mainbanner')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_mainbanner').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'banners': banners,
        # 'form': form,
        'search_query': search_query,
    }
    return render(request, "Al-admin/banner/buy_promo_banner.html", context)

@login_required
def delete_buypromo(request, banner_id):
    if request.method == 'POST':
        try:
            buypromo = MainBanner.objects.get(id=banner_id)
            print(buypromo)
            buypromo.delete()
            return JsonResponse({'message': 'buypromo banner deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'buypromo banner not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    



# # TRENDING BANNER
# @login_required
# def Trending_Banner(request, banner_id=None):
#     # Check if banner_id is provided, if so, get the instance of the banner
#     if banner_id:
#         banner_instance = get_object_or_404(TrendingBrand, pk=banner_id)
#     else:
#         banner_instance = None

#     if request.method == 'POST':
#         # If banner_instance exists, pass it to the form to update the existing banner
#         form =TrendingBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('trendingbanner'))
#     else:
#         # If banner_instance exists, initialize the form with its instance
#         form = TrendingBannerForm(instance=banner_instance)

#     banners = TrendingBrand.objects.all()
    
#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Apply search
#     if search_query:
#         banners = banners.filter(banner_url__icontains=search_query)


#     user_has_permission = request.user.has_perm('banners.view_trendingbanner')

#     # Check group permissions
#     if not user_has_permission:
#         user_groups = request.user.groups.all()
#         for group in user_groups:
#             if group.permissions.filter(codename='view_trendingbanner').exists():
#                 user_has_permission = True
#                 break

#     if not user_has_permission:
#         # Return some error or handle permission denial
#         return render(request, 'Al-admin/permission/permission_denied.html')    

#     context = {
#         'banners': banners,
#         'form': form,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/banner/buy_promo_banner.html", context)

# @login_required
# def delete_buypromo(request, banner_id):
#     if request.method == 'POST':
#         try:
#             buypromo = TrendingBrand.objects.get(id=banner_id)
#             print(buypromo)
#             buypromo.delete()
#             return JsonResponse({'message': 'trending banner deleted successfully'})
#         except Coupon.DoesNotExist:
#             return JsonResponse({'message': 'trending banner not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400)
    

# PRICE BANNER
@login_required
def Price_Banner(request, banner_id=None):
    # Check if banner_id is provided, if so, get the instance of the banner
    if banner_id:
        banner_instance = get_object_or_404( PriceBanner, pk=banner_id)
    else:
        banner_instance = None

    if request.method == 'POST':
        # If banner_instance exists, pass it to the form to update the existing banner
        form = PriceBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pricebanner'))
    else:
        # If banner_instance exists, initialize the form with its instance
        form = PriceBannerForm(instance=banner_instance)


    banners = PriceBanner.objects.all()
    
    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Apply search
    if search_query:
        banners = banners.filter(offer_title__icontains=search_query)


    user_has_permission = request.user.has_perm('banners.view_Price_Banner')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_Price_Banner').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    


    context = {
        'banners': banners,
        'form': form,
        'search_query': search_query,
    }
    return render(request, "Al-admin/banner/price_banner.html", context)
    # return render(request, "Al-admin/banner/offer_banner.html", context)

@login_required
def delete_pricebanner(request, banner_id):
    if request.method == 'POST':
        try:
            offerbanner =  PriceBanner.objects.get(id=banner_id)
            print(offerbanner)
            offerbanner.delete()
            return JsonResponse({'message': 'price banner deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'price banner not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)  
    

#     # craeting
# @login_required
# def footer_Banner(request, banner_id=None):
#     # Check if banner_id is provided, if so, get the instance of the banner
#     if banner_id:
#         banner_instance = get_object_or_404(FooterBanner, pk=banner_id)
#     else:
#         banner_instance = None

#     if request.method == 'POST':
#         # If banner_instance exists, pass it to the form to update the existing banner
#         form = FooterBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('footerbanner'))
#     else:
#         # If banner_instance exists, initialize the form with its instance
#         form = FooterBannerForm(instance=banner_instance)


#     banners = FooterBanner.objects.all()
    
#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Apply search
#     if search_query:
#         banners = banners.filter(
#             # models.Q(banner_head__icontains=search_query) |
#             # models.Q(banner_para__icontains=search_query) |
#             # models.Q(categories__name__icontains=search_query)
#             models.Q(alt_text__icontains=search_query) |
#             models.Q(slot_position__icontains=search_query) 
#             # models.Q(categories__name__icontains=search_query)
#         )


#     Categorys = ParentCategory.objects.all()


#     user_has_permission = request.user.has_perm('banners.view_footerbanner')

#     # Check group permissions
#     if not user_has_permission:
#         user_groups = request.user.groups.all()
#         for group in user_groups:
#             if group.permissions.filter(codename='view_footerbanner').exists():
#                 user_has_permission = True
#                 break

#     if not user_has_permission:
#         # Return some error or handle permission denial
#         return render(request, 'Al-admin/permission/permission_denied.html')    

#     context = {
#         'banners': banners,
#         'form': form,
#         'search_query': search_query,
#         'Categorys': Categorys,
#     }
#     return render(request, "Al-admin/banner/footer_banner.html", context)

# @login_required
# def delete_footerbanner(request, banner_id):
#     if request.method == 'POST':
#         try:
#             footerbanner = FooterBanner.objects.get(id=banner_id)
#             print(footerbanner)
#             footerbanner.delete()
#             return JsonResponse({'message': 'footer banner deleted successfully'})
#         except Coupon.DoesNotExist:
#             return JsonResponse({'message': 'footer banner not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400)  
    


@login_required
def footer_Banner(request, banner_id=None):
    # Check if banner_id is provided, if so, get the instance of the banner
    if banner_id:
        banner_instance = get_object_or_404(FooterBanner, pk=banner_id)
    else:
        banner_instance = None

    if request.method == 'POST':
        # If banner_instance exists, pass it to the form to update the existing banner
        form =FooterBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Buy-Promo-Banner'))
    else:
        # If banner_instance exists, initialize the form with its instance
        form = FooterBannerForm(instance=banner_instance)

    banners = FooterBanner.objects.all()
    
    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Apply search
    if search_query:
        banners = banners.filter(url__icontains=search_query)


    user_has_permission = request.user.has_perm('banners.view_FooterBanner')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_FooterBanner').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'banners': banners,
        # 'form': form,
        'search_query': search_query,
    }
    return render(request, "Al-admin/banner/footer_banner.html", context)

@login_required
def delete_footerbanner(request, banner_id):
    if request.method == 'POST':
        try:
            buypromo = FooterBanner.objects.get(id=banner_id)
            print(buypromo)
            buypromo.delete()
            return JsonResponse({'message': 'FooterBanner deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'FooterBanner  not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
    





























@login_required
def create_group(request, group_id=None):
    # Check if group_id is provided, if so, get the instance of the group
    if group_id:
        group_instance = get_object_or_404(Group, pk=group_id)
    else:
        group_instance = None

    if request.method == 'POST':
        # If group_instance exists, pass it to the form to update the existing group
        form = GroupCreationForm(request.POST, instance=group_instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('group'))
            # return redirect('group_detail', pk=group_instance.pk) if group_instance else redirect('group_list')
    else:
        # If group_instance exists, initialize the form with its instance
        form = GroupCreationForm(instance=group_instance)

    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Retrieve all groups
    groups = Group.objects.all()

    # Apply search if query is provided
    if search_query:
        groups = groups.filter(name__icontains=search_query)

    user_has_permission = request.user.has_perm('auth.view_group')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_group').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'form': form,
        'groups': groups,
        'search_query': search_query,
    }
    return render(request, 'Al-admin/User/create_group.html', context)



@login_required
def delete_group(request, group_id):
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=group_id)
            print(group)
            group.delete()
            return JsonResponse({'message': 'Group deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Group not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)  
    

def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    print(group)
    if request.method == 'POST':
        form = GroupChangeForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            # Redirect or do something else upon successful form submission
            return HttpResponseRedirect(reverse('group'))
    else:
        form = GroupChangeForm(instance=group)
        user_has_permission = request.user.has_perm('auth.view_group')

        # Check group permissions
        if not user_has_permission:
            user_groups = request.user.groups.all()
            for group in user_groups:
                if group.permissions.filter(codename='view_group').exists():
                    user_has_permission = True
                    break

        if not user_has_permission:
            # Return some error or handle permission denial
            return render(request, 'Al-admin/permission/permission_denied.html')   
    return render(request, 'Al-admin/User/edit_group.html', {'form': form})



@login_required
def delivery_person(request, delivery_person_id=None):
    if delivery_person_id:
        # delivery_person_instance = get_object_or_404(OrderDeliveryPerson, pk=delivery_person_id)
        pass
    else:
        delivery_person_instance = None

    if request.method == 'POST':
        form = OrderDeliveryPersonForm(request.POST, instance=delivery_person_instance)
        if form.is_valid():
            # Retrieve the order instance from the form data
            order_instance = form.cleaned_data.get('order')

            # Assign the order instance to the order field of the delivery person
            form.instance.order = order_instance

            form.save()
            return HttpResponseRedirect(reverse('delivery_person'))
    else:
        form = OrderDeliveryPersonForm(instance=delivery_person_instance)

    search_query = request.GET.get('search', '')
    # order_delivery_people = OrderDeliveryPerson.objects.all()

    if search_query:
        order_delivery_people = order_delivery_people.filter(delivery_person_name__icontains=search_query)

    orders = Order.objects.all()

    user_has_permission = request.user.has_perm('checkout.view_orderdeliveryperson')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_orderdeliveryperson').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')

    context = {
        'form': form,
        'order_delivery_people': order_delivery_people,
        'search_query': search_query,
        'orders': orders,
    }
    return render(request, 'Al-admin/collect_person/collect_person.html', context)






@login_required
def delete_delivery_person(request, delivery_person_id):
    print(delivery_person_id)
    if request.method == 'POST':
        try:
            # delivery_person = OrderDeliveryPerson.objects.get(id=delivery_person_id)
            pass
            print(delivery_person)
            delivery_person.delete()
            return JsonResponse({'message': 'Delivery Person deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Delivery Person not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400) 
    




@login_required
def replacement_person(request, replace_collect_person_id=None):
    if replace_collect_person_id:
        # delivery_person_instance = get_object_or_404(ReplacementCollectPerson, pk=replace_collect_person_id)
        pass
    else:
        delivery_person_instance = None

    if request.method == 'POST':
        form = ReplacementCollectPersonForm(request.POST, instance=delivery_person_instance)
        if form.is_valid():
            # Retrieve the order instance from the form data
            order_instance = form.cleaned_data.get('order')

            # Assign the order instance to the order field of the delivery person
            form.instance.order = order_instance

            form.save()
            return HttpResponseRedirect(reverse('replacement_person'))
    else:
        form = ReplacementCollectPersonForm(instance=delivery_person_instance)

    search_query = request.GET.get('search', '')
    # order_replace_people = ReplacementCollectPerson.objects.all()

    if search_query:
        order_replace_people = order_replace_people.filter(collect_person_name__icontains=search_query)

    orders = Order.objects.all()

    user_has_permission = request.user.has_perm('checkout.view_replacementcollectperson')

    # Check group permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_replacementcollectperson').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'form': form,
        'order_replace_people': order_replace_people,
        'search_query': search_query,
        'orders': orders,
    }
    return render(request, 'Al-admin/collect_person/replacement_person.html', context)






@login_required
def delete_replacement_person(request, replace_collect_person_id):
    print(replace_collect_person_id)
    if request.method == 'POST':
        try:
            # delivery_person = ReplacementCollectPerson.objects.get(id=replace_collect_person_id)
            print(delivery_person)
            delivery_person.delete()
            return JsonResponse({'message': 'Re-Collection Person deleted successfully'})
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'Re-Collection Person not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400) 
    



def generate_invoice_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        order_status = request.POST.get('status')

        # Filter orders based on date range and status
        orders = Order.objects.filter(order_date__range=[start_date, end_date])
        if order_status != 'All':
            orders = orders.filter(order_status=order_status)

        # Aggregate data for day-wise reporting
        daily_report = orders.values('order_date').annotate(
            total_orders=Count('id'),
            total_sales=Sum('bill_amount'),
            # total_shipping=Sum('shipping_cost'),
            total_paid=Sum(Case(When(payment_status='paid', then=F('bill_amount')), default=Value(0), output_field=IntegerField())),
            total_pending=Sum(Case(When(payment_status='Pending', then=F('bill_amount')), default=Value(0), output_field=IntegerField())),
            # total_discount=Sum('disc_price'),
            # total_cancelled=Sum('order_status'),
            # total_items=Sum('OrderItem__quentity')
            
        )

        # status = Status.objects.all()

        # invoices = Invoice.objects.filter(invoice_date__range=[start_date, end_date])
        
        # Rendering HTML view
        # context = {'orders': daily_report, 'start_date': start_date, 'end_date': end_date, 'order_status': order_status, 'status':status}
        # return render(request, 'Al-admin/Report/generate_invoice_report.html', context)
    
    # status = Status.objects.all()

    # context = {'status': status}
    
    # return render(request, 'Al-admin/Report/generate_invoice_report.html', context)

def export_invoice_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    if status != 'All':
        orders = orders.filter(payment_status=status)

    # Aggregate data for day-wise reporting
    daily_report = orders.values('order_date').annotate(
        total_orders=Count('id'),
        total_sales=Sum('bill_amount'),
        # total_shipping=Sum('shipping_cost'),
        total_paid=Sum(Case(When(payment_status='paid', then=F('bill_amount')), default=Value(0), output_field=IntegerField())),
        total_pending=Sum(Case(When(payment_status='Pending', then=F('bill_amount')), default=Value(0), output_field=IntegerField())),
        # total_discount=Sum('disc_price'),
        # total_cancelled=Sum('order_status'),
        # total_items=Sum('OrderItem__quentity')
            
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invoice_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Total Orders', 'Invoiced Orders' , 'Total Invoiced', 'Paid Invoices', 'Unpaid Invoices'])

    for entry in daily_report:
        writer.writerow([
            entry['order_date'],
            entry['total_orders'],
            entry['total_orders'],
            entry['total_sales'],
            entry['total_paid'],
            entry['total_pending'],
            # entry['total_discount'],
            # entry['total_cancelled']
        ])
    
    return response




def generate_order_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        order_status = request.POST.get('status')

        # Filter orders based on date range and status
        orders = Order.objects.filter(order_date__range=[start_date, end_date])
        if order_status != 'All':
            orders = orders.filter(order_status=order_status)

        # Aggregate data for day-wise reporting
        daily_report = orders.values('order_date').annotate(
            total_orders=Count('id'),
            total_sales=Sum('bill_amount'),
            total_shipping=Sum('shipping_cost'),
            total_discount=Sum('disc_price'),
            # total_cancelled=Sum('order_status'),
            total_items=Sum('OrderItem__quentity')
        )


        # status = Status.objects.all()

        # context = {'orders': daily_report, 'start_date': start_date, 'end_date': end_date, 'order_status': order_status, 'status':status}
        # return render(request, 'Al-admin/Report/generate_order_report.html', context)
    
    # status = Status.objects.all()

    # context = {'status': status}

    # return render(request, 'Al-admin/Report/generate_order_report.html', context)

def export_order_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    if status != 'All':
        orders = orders.filter(payment_status=status)

    # Aggregate data for day-wise reporting
    daily_report = orders.values('order_date').annotate(
        total_orders=Count('id'),
        total_sales=Sum('bill_amount'),
        total_shipping=Sum('shipping_cost'),
        total_discount=Sum('disc_price'),
        # total_cancelled=Sum('order_status'),
        total_items=Sum('OrderItem__quentity'),
    )

    # Export data as CSV if requested
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Total Orders', 'Total Items' , 'Total Sales', 'Total Shipping', 'Total Discount'])

    for entry in daily_report:
        writer.writerow([
            entry['order_date'],
            entry['total_orders'],
            entry['total_items'],
            entry['total_sales'],
            entry['total_shipping'],
            entry['total_discount'],
            # entry['total_cancelled']
        ])

    return response




def generate_order_shipping_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        order_status = request.POST.get('status')

        # Filter orders based on date range and status
        orders = Order.objects.filter(order_date__range=[start_date, end_date])
        if order_status != 'All':
            orders = orders.filter(order_status=order_status)

        # Aggregate data for day-wise reporting
        daily_report = orders.values('order_date').annotate(
            total_orders=Count('id'),
            # total_sales=Sum('bill_amount'),
            total_shipping=Sum('shipping_cost'),
            # total_discount=Sum('disc_price'),
            # total_cancelled=Sum('order_status'),
            total_items=Sum('OrderItem__quentity')
        )

        # status = Status.objects.all()

        # context = {'orders': daily_report, 'start_date': start_date, 'end_date': end_date, 'order_status': order_status, 'status':status}
        # return render(request, 'Al-admin/Report/generate_order_shipping_report.html', context)
    
    # status = Status.objects.all()

    # context = {'status': status}

    # return render(request, 'Al-admin/Report/generate_order_shipping_report.html', context)

def export_order_shipping_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    if status != 'All':
        orders = orders.filter(payment_status=status)

    # Aggregate data for day-wise reporting
    daily_report = orders.values('order_date').annotate(
        total_orders=Count('id'),
        # total_sales=Sum('bill_amount'),
        total_shipping=Sum('shipping_cost'),
        # total_discount=Sum('disc_price'),
        # total_cancelled=Sum('order_status'),
        total_items=Sum('OrderItem__quentity')
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_shipping_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Total Orders', 'Total Items' , 'Sales Shipping', 'Total Shipping'])

    for entry in daily_report:
        writer.writerow([
            entry['order_date'],
            entry['total_orders'],
            entry['total_items'],
            # entry['total_sales'],
            entry['total_shipping'],
            entry['total_shipping'],
            # entry['total_discount'],
            # entry['total_cancelled']
        ])

    return response



def generate_coupon_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('coupon_start_date')
        end_date = request.POST.get('coupon_end_date')

        # Assuming start_date and end_date are in the format 'YYYY-MM-DD'

        # Query to filter CouponUsage based on date range
        coupon_usage_data = CouponUsage.objects.filter(used_at__range=[start_date, end_date])

        # Aggregate to get count of users who used each coupon
        coupon_usage_count = coupon_usage_data.values('coupon_id').annotate(user_count=Count('user'))

        # Get coupon code, discount values, and used_at date
        coupon_data = coupon_usage_data.values('coupon_id', 'coupon__code', 'coupon__discount_type ', 'used_at').distinct()

        # Prepare the report
        daily_report = []
        for coupon in coupon_data:
            code = coupon['coupon__code']
            discount = coupon['coupon__discount_type ']
            usage_count = next((item['user_count'] for item in coupon_usage_count if item['coupon_id'] == coupon['coupon_id']), 0)
            used_at = coupon['used_at']  # Getting the used_at date
            daily_report.append({'code': code, 'discount': discount, 'user_count': usage_count, 'used_at': used_at})
        
        print(daily_report)

        context = {'orders': daily_report, 'start_date': start_date, 'end_date': end_date}
        return render(request, 'Al-admin/Report/generate_coupon_report.html', context)
    
    # status = Status.objects.all()

    # context = {'status': status}

    return render(request, 'Al-admin/Report/generate_coupon_report.html', context)

def export_coupon_csv(request):
    start_date = request.GET.get('coupon_start_date')
    end_date = request.GET.get('coupon_end_date')
    # status = request.GET.get('status')

    # Query to filter CouponUsage based on date range
    coupon_usage_data = CouponUsage.objects.filter(used_at__range=[start_date, end_date])

    # Aggregate to get count of users who used each coupon
    coupon_usage_count = coupon_usage_data.values('coupon_id').annotate(user_count=Count('user'))

    # Get coupon code, discount values, and used_at date
    coupon_data = coupon_usage_data.values('coupon_id', 'coupon__code', 'coupon__discount_type ', 'used_at').distinct()


    # Prepare the report
    daily_report = []
    for coupon in coupon_data:
        code = coupon['coupon__code']
        discount = coupon['coupon__discount']
        usage_count = next((item['user_count'] for item in coupon_usage_count if item['coupon_id'] == coupon['coupon_id']), 0)
        used_at = coupon['used_at'].date()  # Getting the used_at date
        daily_report.append({'code': code, 'discount': discount, 'user_count': usage_count, 'used_at': used_at})

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_shipping_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Coupon Code', 'Price Rule' , 'Uses', 'Sales Subtotal', 'Sales Discount', 'Sales Total'])

    for entry in daily_report:
        writer.writerow([
            entry['used_at'],
            entry['code'],
            entry['discount_type '],
            entry['user_count'],
            # entry['total_sales'],            
            # entry['total_shipping'],
            # entry['total_discount'],
            # entry['total_cancelled']
        ])

    return response






@login_required
def assign_permissions(request):    

    if request.method == 'POST':
        form = UserPermissionForm(request.POST)
        if form.is_valid():
            # Process the form data and save permissions
            user = form.cleaned_data['user']
            permissions = form.cleaned_data['permissions']
            groups = form.cleaned_data['group']

            if permissions:
                user.user_permissions.set(permissions)
            if groups:
                user.groups.set(groups)

            return HttpResponseRedirect(reverse('permissions'))
    else:
        form = UserPermissionForm()

    # Retrieve search query from request GET parameters
    search_query = request.GET.get('search', '')

    # Retrieve all users
    users = User.objects.all()

    # Apply search if query is provided
    if search_query:
        users = users.filter(username__icontains=search_query)

    user_has_permission = request.user.has_perm('auth.view_user')

    # Check user permissions
    if not user_has_permission:
        user_groups = request.user.groups.all()
        for group in user_groups:
            if group.permissions.filter(codename='view_user').exists():
                user_has_permission = True
                break

    if not user_has_permission:
        # Return some error or handle permission denial
        return render(request, 'Al-admin/permission/permission_denied.html')    

    context = {
        'form': form,
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'Al-admin/User/user_permissions.html', context)


@login_required
def change_permissions(request, user_id):
    # Check if user_id is provided, if so, get the instance of the user
    if user_id:
        user_instance = get_object_or_404(get_user_model(), pk=user_id)
    else:
        user_instance = None

    if request.method == 'POST':
        form = UserPermissionChangeForm(request.POST, instance=user_instance)
        if form.is_valid():
            # Process the form data and save permissions
            permissions = form.cleaned_data['permissions']
            groups = form.cleaned_data['group']
            if permissions:
                user_instance.user_permissions.set(permissions)
            if groups:
                user_instance.groups.set(groups)
            return HttpResponseRedirect(reverse('permissions'))
    else:
        # Get the initial permissions for the user
        initial_permissions = user_instance.user_permissions.all() if user_instance else []
        # Get the initial groups for the user
        initial_groups = user_instance.groups.all() if user_instance else []
        form = UserPermissionChangeForm(instance=user_instance, initial={'permissions': initial_permissions, 'group': initial_groups})


#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Retrieve all users
#     users = get_user_model().objects.all()

#     # Apply search if query is provided
#     if search_query:
#         users = users.filter(username__icontains=search_query)

#     user_has_permission = request.user.has_perm('auth.view_user')

#     # Check user permissions
#     if not user_has_permission:
#         user_groups = request.user.groups.all()
#         for group in user_groups:
#             if group.permissions.filter(codename='view_user').exists():
#                 user_has_permission = True
#                 break

#     if not user_has_permission:
#         # Return some error or handle permission denial
#         return render(request, 'Al-admin/permission/permission_denied.html')

#     context = {
#         'form': form,
#     }
#     return render(request, 'Al-admin/User/change_user_permissions.html', context)



# def robots_txt_view(request, robots_id=None):
#     if robots_id:
#         # Fetch the category instance if the category_id is provided
#         robots_instance = get_object_or_404(RobotsTxt, pk=robots_id)
#     else:
#         robots_instance = None
    
#     if request.method == 'POST':
#         if robots_instance:
#             # Call the category update view
#             form = RobotsTxtForm(data=request.POST, instance=robots_instance)
#         else: 
#             # Create a new category using the POST data
#             form = RobotsTxtForm(data=request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('robots')  # Redirect to a success page
#     else:
#         form = RobotsTxtForm(instance=robots_instance)

#     robots_txt = RobotsTxt.objects.all()  # Assuming there's only one instance

#     context = {
#         'form':form,
#         'robots_txt': robots_txt,
#     }

#     return render(request, 'Al-admin/seo_settings/robots_txt.html', context)

# def google_tag_manager_view(request, gtm_id=None):
    
#     if gtm_id:
#         # Fetch the category instance if the category_id is provided
#         gtm_instance = get_object_or_404(GoogleTagManager, pk=gtm_id)
#     else:
#         robots_instance = None
    
#     if request.method == 'POST':
#         if robots_instance:
#             # Call the category update view
#             form = GoogleTagManagerForm(data=request.POST, instance=robots_instance)
#         else: 
#             # Create a new category using the POST data
#             form = GoogleTagManagerForm(data=request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  # Redirect to a success page
#     else:
#         form = GoogleTagManagerForm(instance=robots_instance)

#     google_tag_manager = GoogleTagManager.objects.all()  # Assuming there's only one instance
#     context = {
#         'form':form,
#         'google_tag_manager': google_tag_manager,
#     }
#     return render(request, 'Al-admin/seo_settings/google_tag_manager.html', context)


# def robots_txt_delete(request, robots_id):
#     robots_instance = get_object_or_404(RobotsTxt, pk=robots_id)
#     if request.method == 'POST':
#         robots_instance.delete()
#         return redirect('robots')  # Redirect after deletion
#     return render(request, 'confirm_delete.html', {'object': robots_instance})

# def google_tag_manager_delete(request, gtm_id):
#     gtm_instance = get_object_or_404(GoogleTagManager, pk=gtm_id)
#     if request.method == 'POST':
#         gtm_instance.delete()
#         return redirect('success_url')  # Redirect after deletion
#     return render(request, 'confirm_delete.html', {'object': gtm_instance})




# @login_required
# def category_Banner(request, banner_id=None):
#     # Check if banner_id is provided, if so, get the instance of the banner
#     if banner_id:
#         banner_instance = get_object_or_404(categorybanner, pk=banner_id)
#     else:
#         banner_instance = None

#     if request.method == 'POST':
#         # If banner_instance exists, pass it to the form to update the existing banner
#         form = CategoryBannerForm(data=request.POST, files=request.FILES, instance=banner_instance)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('categorybanner'))
#     else:
#         # If banner_instance exists, initialize the form with its instance
#         if banner_instance:
#             # If banner_instance exists, initialize the form with its instance
#             initial_data = {'Category': banner_instance.Category}
#         else:
#             initial_data = {}
#         form = CategoryBannerForm(instance=banner_instance, initial=initial_data)


#     banners = categorybanner.objects.all()
    
#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')

#     # Apply search
#     if search_query:
#         banners = banners.filter(Category__name__icontains=search_query)


#     user_has_permission = request.user.has_perm('banners.view_categorybanner')

#     # Check group permissions
#     if not user_has_permission:
#         user_groups = request.user.groups.all()
#         for group in user_groups:
#             if group.permissions.filter(codename='view_categorybanner').exists():
#                 user_has_permission = True
#                 break

#     if not user_has_permission:
#         # Return some error or handle permission denial
#         return render(request, 'Al-admin/permission/permission_denied.html')    


#     context = {
#         'banners': banners,
#         'form': form,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/banner/category_banner.html", context)

# @login_required
# def delete_categorybanner(request, banner_id):
#     if request.method == 'POST':
#         try:
#             category_banner = categorybanner.objects.get(id=banner_id)
#             print(category_banner)
#             category_banner.delete()
#             return JsonResponse({'message': 'category banner deleted successfully'})
#         except Coupon.DoesNotExist:
#             return JsonResponse({'message': 'category banner not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400) 
    


# @login_required
# def offer_admin(request, offer_id=None):
#     if offer_id:
#         # Fetch the offer instance if the offer_id is provided
#         offer_instance = get_object_or_404(Offer, pk=offer_id)
#     else:
#         offer_instance = None
    
#     if request.method == 'POST':
#         if offer_instance:
#             # If a POST request is made with offer_id, update the existing record
#             form = OfferForm(request.POST, instance=offer_instance)
#         else:
#             # Otherwise create a new record
#             form = OfferForm(request.POST)
        
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('offer-admin'))
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form = OfferForm(instance=offer_instance)

#     # Retrieve offer values
#     offers = Offer.objects.all()

#     # Retrieve search query from request GET parameters
#     search_query = request.GET.get('search', '')
#     print(search_query)

#     # Apply search
#     if search_query:
#         offers = offers.filter(Q(name__icontains=search_query))

#     context = {
#         'offers': offers,
#         'form': form,
#         'search_query': search_query,
#     }
#     return render(request, "Al-admin/product/offer-admin.html", context)


# def offer_update_view(request, id):
#     offer = get_object_or_404(Offer, id=id)
#     if request.method == 'POST':
#         form = OfferForm(request.POST, request.FILES, instance=offer)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or handle as needed
#             return redirect('offer-admin')
#     else:
#         form = OfferForm(instance=offer)
#     return render(request, 'Al-admin/product/offer-update.html', {'form': form, 'offers': offer})






# @login_required
# def delete_offer(request, offer_id):
#     if request.method == 'POST':
#         try:
#             offer = Offer.objects.get(id=offer_id)
#             print(offer)
#             offer.delete()
#             return JsonResponse({'message': 'Offer deleted successfully'})
#         except Offer.DoesNotExist:
#             return JsonResponse({'message': 'Offer not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400)