from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.results import RowResult
from import_export.admin import ImportExportModelAdmin
from .models import *
from product.models import *
# Register your models here.
# admin.site.register(MainBanner)
# admin.site.register(TrendingBrand)
# admin.site.register(FooterBanner)


class MainBannerResource(resources.ModelResource):
    class Meta:
        model = MainBanner

@admin.register(MainBanner)
class MainBannerAdmin(ImportExportModelAdmin):
    resource_class = MainBannerResource
    list_display = ('url', 'slot_position', 'active')

class TrendingBrandResource(resources.ModelResource):
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=widgets.ForeignKeyWidget(Brand, 'name')
    )

    class Meta:
        model = TrendingBrand
        fields = ('brand', 'brand_image', 'alt_text', 'url', 'slot_position', 'active')
        import_id_fields = ('brand', 'brand_image', 'url', 'slot_position')  # Assuming combination of brand and url is unique

    def before_import_row(self, row, **kwargs):
        brand_name = row.get('brand')
        if not Brand.objects.filter(name=brand_name).exists():
            raise ValueError(f"Brand with name '{brand_name}' does not exist.")

    def import_row(self, row, instance_loader, **kwargs):
        try:
            return super().import_row(row, instance_loader, **kwargs)
        except ValueError as e:
            result = RowResult()
            result.import_type = RowResult.IMPORT_TYPE_ERROR
            result.errors.append((str(e),))
            return result

@admin.register(TrendingBrand)
class TrendingBrandAdmin(ImportExportModelAdmin):
    resource_class = TrendingBrandResource
    list_display = ('brand', 'url', 'slot_position', 'active')

class FooterBannerResource(resources.ModelResource):
    class Meta:
        model = FooterBanner

@admin.register(FooterBanner)
class FooterBannerAdmin(ImportExportModelAdmin):
    resource_class = FooterBannerResource
    list_display = ('url', 'slot_position', 'active')


admin.site.register(PriceBanner)

admin.site.register(WhyUs)