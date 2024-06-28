from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
import csv
import os
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.



# admin.site.register(ParentCategory)
# admin.site.register(SubCategory)
# admin.site.register(ChildSubCategory)
# admin.site.register(Brand)


class ParentCategoryResource(resources.ModelResource):
    class Meta:
        model = ParentCategory

@admin.register(ParentCategory)
class ParentCategoryAdmin(ImportExportModelAdmin):
    resource_class = ParentCategoryResource
    list_display = ('name', 'slug', 'active')

class ParentCategoryWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        try:
            return self.get_queryset(value, row, **kwargs).get(**{self.field: value})
        except self.model.DoesNotExist:
            raise ValueError(f"ParentCategory with name '{value}' does not exist.")

class SubCategoryResource(resources.ModelResource):
    parent_category = fields.Field(
        column_name='parent_category',
        attribute='parent_category',
        widget=ParentCategoryWidget(ParentCategory, 'name')
    )

    class Meta:
        model = SubCategory
        fields = ('parent_category', 'name', 'image', 'slot_position', 'skin_routine')
        import_id_fields = ('parent_category', 'name', 'image', 'slot_position', 'skin_routine')

    def before_import_row(self, row, **kwargs):
        parent_category_name = row.get('parent_category')
        if not ParentCategory.objects.filter(name=parent_category_name).exists():
            raise ValueError(f"ParentCategory with name '{parent_category_name}' does not exist.")

    def import_row(self, row, instance_loader, **kwargs):
        try:
            return super().import_row(row, instance_loader, **kwargs)
        except ValueError as e:
            result = RowResult()
            result.import_type = RowResult.IMPORT_TYPE_ERROR
            result.errors.append((str(e),))
            return result

@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('name', 'slug', 'parent_category', 'skin_routine', 'active')

class ChildSubCategoryResource(resources.ModelResource):
    class Meta:
        model = ChildSubCategory

@admin.register(ChildSubCategory)
class ChildSubCategoryAdmin(ImportExportModelAdmin):
    resource_class = ChildSubCategoryResource
    list_display = ('name', 'slug', 'sub_category', 'active')

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    resource_class = BrandResource
    list_display = ('name', 'slug', 'active')



class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class productImageInline(admin.TabularInline):
    list_display = ('product', 'image')
    model = ProductImage
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'sku', 'published', 'in_stock', 'stock', 'low_stock_amount', 'sale_price', 'regular_price', 'weight', 'length', 'width', 'height', 'allow_customer_reviews', 'seo_title', 'seo_keyword', 'seo_description')

    def display_subcategories(self, obj):
        return ", ".join([subcategory.name for subcategory in obj.subcategories.all()])

    def display_childsubcategories(self, obj):
        return ", ".join([childsubcategory.name for childsubcategory in obj.childsubcategories.all()])

    def display_brands(self, obj):
        return ", ".join([brand.name for brand in obj.brands.all()])

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    display_subcategories.short_description = 'Subcategories'
    display_childsubcategories.short_description = 'Child Subcategories'
    display_brands.short_description = 'Brands'
    display_tags.short_description = 'Tags'

    list_filter = ('type', 'published', 'in_stock', 'brands', 'categories', 'subcategories', 'childsubcategories')
    search_fields = ('name', 'sku', 'subcategories__name' , 'childsubcategories__name', 'brands__name')
    change_list_template = 'admin/product/Product/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("upload-csv/", self.upload_csv),
            # path("download-sample-xls/", self.download_sample_xls),
            # path("download_sample_csv/", self.download_sample_csv),
            # path('export-xls/', self.export_to_xls),
            # path('export_to_csv/', self.export_to_csv)
        ]
        return my_urls + urls
    
    def upload_csv(self, request):
        if request.method == "POST" and "csv_upload" in request.FILES:
            try:
                file = request.FILES["csv_upload"]
                if not file.name.endswith(('.csv', '.xls', '.xlsx')):
                    return HttpResponse("Invalid file format. Please upload a CSV or Excel file.")

                if file.name.endswith('.csv'):
                    data = file.read().decode("utf-8")
                    csv_data = csv.reader(data.splitlines())

                    # Read and skip the header row
                    header = next(csv_data)

                    for row in csv_data:
                        # Extract data from CSV row
                        type = row[0]
                        sku = row[1]
                        name = row[2]
                        published = row[3]
                        short_description = row[4]
                        description = row[5]
                        in_stock = row[6]

                        # Convert empty strings to default integer values
                        stock = int(row[7]) if row[7].strip() else 0
                        low_stock_amount = int(row[8]) if row[8].strip() else 0
                        sale_price = None if row[9].strip() == '' else float(row[9])
                        regular_price = float(row[10].strip()) if row[10].strip() else 0.0

                        weight_str = row[11].strip() if len(row) > 11 else ''
                        length_str = row[12].strip() if len(row) > 12 else ''
                        width_str = row[13].strip() if len(row) > 13 else ''
                        height_str = row[14].strip() if len(row) > 14 else ''

                        # Convert strings to appropriate types, handle missing values
                        try:
                            weight = float(weight_str) if weight_str else None
                        except ValueError:
                            weight = None

                        try:
                            length = float(length_str) if length_str else None
                        except ValueError:
                            length = None

                        try:
                            width = float(width_str) if width_str else None
                        except ValueError:
                            width = None

                        try:
                            height = float(height_str) if height_str else None
                        except ValueError:
                            height = None

                        allow_customer_reviews = row[15] == 'TRUE'
                        
                        # Check if image_paths column exists and is not empty
                        if len(row) > 16 and row[16].strip():
                            image_paths = row[16].split(',')
                        else:
                            image_paths = []

                        # Split categories, subcategories, child subcategories, and brand based on comma separator
                        categories = row[17].split(',') if len(row) > 17 else []
                        subcategories = row[18].split(',') if len(row) > 18 else []
                        child_subcategories = row[19].split(',') if len(row) > 19 else []
                        brands = row[20].split(',') if len(row) > 20 else []
                        tags = row[21].split(',') if len(row) > 21 else []

                        # Handle categories, subcategories, child subcategories, and brands
                        # for category_name in categories:
                        #     category, _ = ParentCategory.objects.get_or_create(name=category_name.strip())
                        #     product.categories.add(category)

                        # for subcategory_name in subcategories:
                        #     subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name.strip())
                        #     product.subcategories.add(subcategory)

                        # for child_subcategory_name in child_subcategories:
                        #     child_subcategory, _ = ChildSubCategory.objects.get_or_create(name=child_subcategory_name.strip())
                        #     product.child_subcategories.add(child_subcategory)

                        # for brand_name in brands:
                        #     brand, _ = Brand.objects.get_or_create(name=brand_name.strip())
                        #     product.brand.add(brand)


                        # Create or update Product instance
                        # product, created = Product.objects.update_or_create(
                        #     sku=sku,
                        #     defaults={
                        #         'type': type,
                        #         'name': name,
                        #         'published': published,
                        #         'short_description': short_description,
                        #         'description': description,
                        #         'in_stock': in_stock,
                        #         'stock': stock,
                        #         'low_stock_amount': low_stock_amount,
                        #         'sale_price': sale_price,
                        #         'regular_price': regular_price,
                        #         'weight': weight,
                        #         'length': length,
                        #         'width': width,
                        #         'height': height,
                        #         'allow_customer_reviews': allow_customer_reviews,
                        #     }
                        # )

                        products = Product.objects.create(
                            
                                type= type,
                                sku=sku,
                                name= name,
                                published=published,
                                short_description=short_description,
                                description=description,
                                in_stock=in_stock,
                                stock=stock,
                                low_stock_amount=low_stock_amount,
                                sale_price=sale_price,
                                regular_price=regular_price,
                                weight=weight,
                                length=length,
                                width=width,
                                height=height,
                                allow_customer_reviews=allow_customer_reviews,
                            
                        )
                        print(products)
                        # Handle categories, subcategories, child subcategories, and brands

                        # Check and process categories
                        if categories:
                            for category_name in categories:
                                print(category_name)
                                category, _ = ParentCategory.objects.get_or_create(name=category_name.strip())
                                products.categories.add(category)

                        # Check and process brands
                        if brands:
                            for brand_name in brands:
                                brand, _ = Brand.objects.get_or_create(name=brand_name.strip())
                                products.brands.add(brand)
                                print(brand_name)

                        # Check and process tags
                        if tags:
                            for tag_name in tags:
                                # Check if the tag starts with "#" or not
                                if not tag_name.startswith('#'):
                                    tag_name = '#' + tag_name.strip()  # Add "#" prefix
                                tag, _ = Tag.objects.get_or_create(name=tag_name)
                                products.tags.add(tag)
                                print(tag_name)

                        # Check and process subcategories
                        if subcategories:
                            for subcategory_name in subcategories:
                                try:
                                    subcategory = SubCategory.objects.get(name=subcategory_name.strip())
                                    products.subcategories.add(subcategory)
                                    print(subcategory_name)
                                except ObjectDoesNotExist:
                                    print(f"Subcategory '{subcategory_name}' does not exist")

                        # Check and process child subcategories
                        if child_subcategories:
                            for child_subcategory_name in child_subcategories:
                                try:
                                    child_subcategory = ChildSubCategory.objects.get(name=child_subcategory_name.strip())
                                    products.childsubcategories.add(child_subcategory)
                                    print(child_subcategory_name)
                                except ObjectDoesNotExist:
                                    print(f"Child subcategory '{child_subcategory_name}' does not exist")

                        

                        created = True
                        # Assuming `image_paths` is a list of image paths to be added
                        for i, image_path in enumerate(image_paths):
                            if image_path.strip():  # Only process non-empty image paths
                                image_path = os.path.join('product_images', image_path.strip('/'))

                                # Create a new ProductImage instance
                                product_image = ProductImage(
                                    product=products,
                                    image=image_path,
                                    slot_position=i
                                )
                                product_image.save()

                                print(f'New image added for product {products.name}: {image_path}')

                        # # Save product images, skipping any empty image paths
                        # for i, image_path in enumerate(image_paths):
                        #     if image_path.strip():  # Only process non-empty image paths
                        #         image = ProductImage(product=product, image=image_path.strip(), slot_position=i)
                        #         image.save()
                
                return HttpResponseRedirect('/admin/product/product/')
            
            except Exception as e:
                return HttpResponse(f"Error occurred: {str(e)}")
        
        form = CsvImportForm()
        data = {"form": form}

        return render(request, 'admin/csv_upload.html', data)

    inlines = [productImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Tag)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(UpsellProduct)
admin.site.register(CrossSellProduct)
admin.site.register(ComboProduct)