from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import *
from rating.models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.cache import cache_control

from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.views.generic import ListView



# Create your views here.

media_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)

def brands(request):
    brands = Brand.objects.all().order_by('name')
    grouped_brands = {}

    for brand in brands:
        # print(brand.name)
        if brand.name:  # Ensure the name is not empty
            initial = brand.name[0].upper()
            # print(initial)
            if initial not in grouped_brands:
                grouped_brands[initial] = []
            grouped_brands[initial].append(brand)
    context = {
        'grouped_brands': grouped_brands
    }
    return render(request, 'products/brands.html', context)

def product_list(request, categoryslug=None,subcategoryslug=None,childsubcategoryslug=None,brandslug=None):
    if brandslug:
        brand = get_object_or_404(Brand, slug=brandslug)
        products = Product.objects.filter(brands=brand, published='Published').order_by('name')
        breadcrumbs = [
            {'text': 'Home', 'url': '/'},  # Link to the homepage
            {'text': 'BRANDS', 'url': f'/brands/'},  # Link to the Brands page
            {'text': brand, 'url': f'/product-category/{brandslug}/'},  # Link to the Brands products page
        ]
        data_id = brand

    elif childsubcategoryslug:
        parent_category = get_object_or_404(ParentCategory, slug=categoryslug)
        sub_category = get_object_or_404(SubCategory, slug=subcategoryslug)
        child_subcategory = get_object_or_404(ChildSubCategory, slug=childsubcategoryslug)
        products = Product.objects.filter(categories=parent_category, subcategories=sub_category, childsubcategories=child_subcategory, published='Published').order_by('name')
        breadcrumbs = [
            {'text': 'Home', 'url': '/'},  # Link to the homepage
            {'text': parent_category, 'url': f'/product-category/{categoryslug}/'},  # Link to the category page
            {'text': sub_category, 'url': f'/product-category/{categoryslug}/{subcategoryslug}/'},  # Link to the subcategory page
            {'text': child_subcategory, 'url': f'/product-category/{categoryslug}/{subcategoryslug}/{child_subcategory}/'},  # Link to the subcategory page
        ]
        data_id = child_subcategory

    elif subcategoryslug:
        parent_category = get_object_or_404(ParentCategory, slug=categoryslug)
        sub_category = get_object_or_404(SubCategory, slug=subcategoryslug)
        products = Product.objects.filter(categories=parent_category, subcategories=sub_category, published='Published').order_by('name')
        breadcrumbs = [
            {'text': 'Home', 'url': '/'},  # Link to the homepage
            {'text': parent_category, 'url': f'/product-category/{categoryslug}/'},  # Link to the category page
            {'text': sub_category, 'url': f'/product-category/{categoryslug}/{subcategoryslug}/'},  # Link to the subcategory page
        ]
        data_id = sub_category
    else:
        parent_category = get_object_or_404(ParentCategory, slug=categoryslug)
        products = Product.objects.filter(categories=parent_category, published='Published').order_by('name')
        breadcrumbs = [
            {'text': 'Home', 'url': '/'},  # Link to the homepage
            {'text': parent_category, 'url': f'/product-category/{categoryslug}/'},  # Link to the category page
        ]
        data_id = parent_category
    
    print('products', products)
    context = {
        'products':products,
        'breadcrumbs':breadcrumbs,
        'data_id':data_id,
    }
    return render(request, 'products/product_list.html', context)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_cat_sort_value(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sort_value = data.get('sortValue')
        data_id = data.get('data_id')
        page_number = data.get('page', 1)

        print(f"Received sort value: {sort_value}")
        print(f"Received category ID: {data_id}")
        print(f"Received page number: {page_number}")

        products = Product.objects.filter(published='Published')

        category_filtered = False

        if data_id:
            try:
                category = ParentCategory.objects.get(name=data_id)
                products = products.filter(categories=category)
                category_filtered = True
            except ParentCategory.DoesNotExist:
                pass

            if not category_filtered:
                try:
                    subcategory = SubCategory.objects.get(name=data_id)
                    products = products.filter(subcategories=subcategory)
                    category_filtered = True
                except SubCategory.DoesNotExist:
                    pass

            if not category_filtered:
                try:
                    childsubcategory = ChildSubCategory.objects.get(name=data_id)
                    products = products.filter(childsubcategories=childsubcategory)
                    category_filtered = True
                except ChildSubCategory.DoesNotExist:
                    pass

            if not category_filtered:
                try:
                    brand = Brand.objects.get(name=data_id)
                    products = products.filter(brands=brand)
                except Brand.DoesNotExist:
                    pass
        print(f"Filtered products query count: {products.count()}")
        if sort_value == 'Low to High':
            products = products.order_by('regular_price')
        elif sort_value == 'High to Low':
            products = products.order_by('-regular_price')
        elif sort_value == 'latest':
            products = products.order_by('-created_at')
        elif sort_value == 'Popularity':
            products = products.order_by('-popularity')
        filtered_products = []
        for product in products:
            product_data = {
                'name': product.name,
                'regular_price': product.regular_price,
                'id': product.id,
                'created_at': product.created_at,
                'sale_price': product.sale_price,
                'images': []
            }

            # Get images for the product
            product_images = ProductImage.objects.filter(product=product).order_by('slot_position')
            print(f"Product ID {product.id} has {product_images.count()} images")

            for image in product_images:
                print(f"Image URL: {image.image.url}, Alt text: {image.alt_text}")
                product_data['images'].append({
                    'url': image.image.url,
                    'alt_text': image.alt_text
                })

            filtered_products.append(product_data)
        
        response_data = {
            'products': filtered_products,
        }

        print(response_data)  # Print the response data to debug

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'})


# def product_details(request, slug):
#     # Get the product with the given slug
#     product = get_object_or_404(Product, slug=slug)
#     print(product)

#     # Get the previous product by ID
#     previous_product = Product.objects.filter(id__lt=product.id).order_by('-id').first()

#     # Get the next product by ID
#     next_product = Product.objects.filter(id__gt=product.id).order_by('id').first()


#     upsell_product_relation = UpsellProduct.objects.filter(product=product, active=True).first()
#     you_may_like = upsell_product_relation.upsell_products.all() if upsell_product_relation else []
#     print('you_may_like', you_may_like)


#     product_categories = product.categories.all()
#     product_subcategories = product.subcategories.all()
#     product_childsubcategories = product.childsubcategories.all()

#     related_products = Product.objects.filter(
#         models.Q(categories__in=product_categories) |
#         models.Q(subcategories__in=product_subcategories) |
#         models.Q(childsubcategories__in=product_childsubcategories)
#     ).distinct().exclude(id=product.id)[:8]

#     print('related_products', related_products)


#     ratings = Rating.objects.filter(product=product)
#     rating_count = ratings.count()


#     # # Assume the product model has relationships to category, subcategory, and child category
#     # category = product.categories
#     # subcategory = product.subcategories
#     # child_category = product.childsubcategories

#     # # Construct the breadcrumbs
#     # breadcrumbs = [
#     #     {'text': 'Home', 'url': '/'},  # Link to the homepage
#     #     {'text': category.name, 'url': f'/product-category/{category.slug}/'},  # Link to the category page
#     #     {'text': subcategory.name, 'url': f'/product-category/{category.slug}/{subcategory.slug}/'},  # Link to the subcategory page
#     #     {'text': child_category.name, 'url': f'/product-category/{category.slug}/{subcategory.slug}/{child_category.slug}/'},  # Link to the child category page
#     #     {'text': product.name, 'url': f'/product/{product.slug}/'}  # Link to the product page
#     # ]

#     # # Print the product and breadcrumbs for debugging
#     # print(product)
#     # print(breadcrumbs)


#     context = {
#         'product':product,
#         # 'breadcrumbs':breadcrumbs,
#         'previous_product':previous_product,
#         'next_product':next_product,
#         'you_may_like':you_may_like,
#         'related_products':related_products,
#         'ratings':ratings,
#         'rating_count':rating_count,

#     }
#     return render(request, 'products/product_details.html', context)



def product_details(request, slug):
    # Get the product with the given slug
    product = get_object_or_404(Product, slug=slug)
    print(product)

    # Check if the product is part of a combo product
    combo_product = ComboProduct.objects.filter(product=product, active=True).first()
    combo_products = combo_product.Combo_products.all() if combo_product else []

    # Get the previous product by ID
    previous_product = Product.objects.filter(id__lt=product.id).order_by('-id').first()

    # Get the next product by ID
    next_product = Product.objects.filter(id__gt=product.id).order_by('id').first()

    upsell_product_relation = UpsellProduct.objects.filter(product=product, active=True).first()
    you_may_like = upsell_product_relation.upsell_products.all() if upsell_product_relation else []
    print('you_may_like', you_may_like)

    product_categories = product.categories.all()
    product_subcategories = product.subcategories.all()
    product_childsubcategories = product.childsubcategories.all()

    related_products = Product.objects.filter(
        models.Q(categories__in=product_categories) |
        models.Q(subcategories__in=product_subcategories) |
        models.Q(childsubcategories__in=product_childsubcategories)
    ).distinct().exclude(id=product.id)[:8]

    print('related_products', related_products)

    ratings = Rating.objects.filter(product=product)
    rating_count = ratings.count()

    combo_product_details = []
    for combo_item in combo_products:
        images = ProductImage.objects.filter(product=combo_item)
        combo_product_details.append({
            'product': combo_item,
            'images': images,
        })

    context = {
        'product': product,
        'previous_product': previous_product,
        'next_product': next_product,
        'you_may_like': you_may_like,
        'related_products': related_products,
        'ratings': ratings,
        'rating_count': rating_count,
        'combo_product': combo_product,
        'combo_product_details': combo_product_details,
    }

    return render(request, 'products/product_details.html', context)



@csrf_exempt
def get_product_data(request):
    if request.method == 'POST':
        # product_id = request.POST.get('id')
        data = json.loads(request.body)
        product_id = data.get('id')

        print(product_id)
        product = Product.objects.get(id=product_id)
        product_data = {
            'name': product.name,
            'regular_price': product.regular_price,
            'sale_price': product.sale_price,
            'description': product.description,
            'sku': product.sku,
            'images': [{'image_url': image.image.url} for image in product.images.all()],
        }
        return JsonResponse(product_data)



class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        print(category_id)
        category = ParentCategory.objects.get(name=category_id)
        queryset = Product.objects.filter(categories=category, published='Published').order_by('regular_price')
        print(queryset)
        return queryset
    



# from django.shortcuts import render
# from .models import Product

# def product_list(request):
#     product_count = request.GET.get('count')
#     # products=Product.objects.all()[:product_count] 
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return JsonResponse("jfdytruytruy")
#     if product_count:
#          product_count = int(product_count)
#          print(type(product_count))
#          products=Product.objects.all()[:product_count] 
#     else:
#         products=Product.objects.all()
#     context = {
#         'products': products,
#         'selected_count': product_count,
#     }
#     print(context)
#     return render(request, 'products/product_list.html', context)

          
    # return render(request, 'products/productslist.html', context)
    # return render(request, 'products/product_list.html', context)

# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from .models import Product

# def product_list(request):
#     product_count = request.GET.get('count')
#     sort_value = request.GET.get('sort_value')
#     if sort_value == 'low-to-high':
#         products = products.order_by('regular_price')
#         print(products)
#     elif sort_value == 'high-to-low':
#         products = products.order_by('-regular_price')
#     # selected_value = request.GET.get('counts')
#     # product_filter= Product.objects.filter( Products__regular_price)
#     if product_count:
#         product_count = int(product_count)
#         products = Product.objects.all()[:product_count]
        
#     else:
#         products = Product.objects.all()
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('products/productslist.html', {'products': products})
#         return JsonResponse({'html': html})
    
#     context = {
#         'products': products,
#         'selected_count': product_count,
#         'sort_value': sort_value,
#     }
#     return render(request, 'products/product_list.html', context)





# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from .models import Product

# def product_list(request):
#     product_count = request.GET.get('count')
#     sort_value = request.GET.get('sort_value')
    
#     # category = ParentCategory.objects.get(name='skincare')
#     # print(category)
#     category = ParentCategory.objects.get(name='skincare')
#     # print(category)
#     # products = products.filter(categories=category)
#     # category_filtered = True
#     # except ParentCategory.DoesNotExist:
#     # pass

#     if category:
#         products=Product.objects.all(categories=category)
#     products = Product.objects.all( )
#     # products_value=Product.objects.filter()
#     if sort_value == 'Low to High':
#         products = products.order_by('regular_price')
#     elif sort_value == 'High to Low':
#         products = products.order_by('-regular_price')
#     if product_count:
#         product_count = int(product_count)
#         products = products[:product_count]
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('products/productslist.html', {'products': products})
#         return JsonResponse({'html': html})

#     context = {
#         'products': products,
#         'selected_count': product_count,
#         'sort_value': sort_value,
#     }
#     return render(request, 'products/product_list.html', context) 

# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from django.shortcuts import render
# from .models import Product, ParentCategory

# def product_list(request):
#     product_count = request.GET.get('count')
#     sort_values = request.GET.get('sort_values' ,'low to high')
#     try:
#         category = ParentCategory.objects.get(name='accessories')
#     except ParentCategory.DoesNotExist:
#         category = None

#     if category:
#         products = Product.objects.filter(categories=category)
#         print(products)
#         # products1=products.order_by('regular_price')
#         # print(products1)

#     else:
#         products = Product.objects.all()
#         print('products give me', products)

#     if sort_values == 'Low to High':
#         products = products.order_by('regular_price')
#     elif sort_values == 'High to Low':
#         products = products.order_by('-regular_price')

#     if product_count:
#         try:
#             product_count = int(product_count)
#             products = products[:product_count]
#         except ValueError:
#             pass  

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('products/productslist.html', {'products': products})
#         return JsonResponse({'html': html})

#     context = {
#         'products': products,
#         'selected_count': product_count,
#         'sort_values': sort_values,
#     }
#     return render(request, 'products/product_list.html', context)

# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from django.shortcuts import render
# from .models import Product, ParentCategory

# def product_list(request):
#     product_count = request.GET.get('count')
#     sort_values = request.GET.get('sort_values')

#     try:
#         category = ParentCategory.objects.get(name='accessories')
#     except ParentCategory.DoesNotExist:
#         category = None
#     if category:
#         products = Product.objects.filter(categories=category)
#     else:
#         products = Product.objects.all()
#     if sort_values == 'Low to High':
#         products = products.order_by('regular_price').first()
#     elif sort_values == 'High to Low':
#         products = products.order_by('-regular_price')

#     if product_count:
        
#         try:
#             product_count = int(product_count)
#             products = products[:product_count].first()

#         except ValueError:
#             pass  

#     # if product_count:
#     #     try:
#     #         product_count = int(product_count)
#     #         if product_count == 1:
#     #             product = products.first()  
#     #             products = [product] if product else []  
#     #         else:
#     #             products = products[:product_count]  
#     #     except ValueError:
#     #         products = products.all()  

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('products/productslist.html', {'products': products})
#         return JsonResponse({'html': html})

#     context = {
#         'products': products,
#         'selected_count': product_count,
#         'sort_values': sort_values,
#     }
#     return render(request, 'products/product_list.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from .models import Product, ParentCategory

def product_list(request):
    product_count = request.GET.get('count')
    sort_values = request.GET.get('sort_values')

    try:
        category = ParentCategory.objects.get(name='accessories')
    except ParentCategory.DoesNotExist:
        category = None
    
    # Filter products based on category
    if category:
        products = Product.objects.filter(categories=category)
    else:
        products = Product.objects.all()

    # Sort products based on the sort_values parameter
    if sort_values == 'Low to High':
        products = products.order_by('regular_price')
    elif sort_values == 'High to Low':
        products = products.order_by('-regular_price')

    # Apply product_count if provided
    if product_count:
        try:
            product_count = int(product_count)
            if product_count > 0:
                products = products[:product_count]
        except ValueError:
            pass 

    # Render the response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('products/productslist.html', {'products': products})
        return JsonResponse({'html': html})

    context = {
        'products': products,
        'selected_count': product_count,
        'sort_values': sort_values,
    }
    return render(request, 'products/product_list.html', context)




# i wnat category  based count products diplay on my page

# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from .models import Product

# def product_list(request):
#     product_count = request.GET.get('count')
#     sort_value = request.GET.get('sort_value')

#     products = Product.objects.all()
#     if sort_value == 'low-to-high':
#         products = products.order_by('price')
#     elif sort_value == 'high-to-low':
#         products = products.order_by('-price')
#     if product_count:
#         product_count = int(product_count)
#         products = products[:product_count]

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('products/productslist.html', {'products': products})
#         return JsonResponse({'html': html})

#     context = {
#         'products': products,
#         'selected_count': product_count,
#         'sort_value': sort_value,
#     }
#     return render(request, 'products/product_list.html', context)


# # 2nd method sectiom 
    # product_count = int(request.GET.get('count',0))
    # if product_count == 0:
    #    products=Product.objects.all()
    # else:
    #    products=Product.objects.all()[:product_count] 
