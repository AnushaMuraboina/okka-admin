from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('brands/',views.brands, name='brands'),
   path('product-category/brands/<slug:brandslug>/', views.product_list, name="product-brand"),
   path('product-category/<slug:categoryslug>/', views.product_list, name="product-category"),
   path('product-category/<slug:categoryslug>/<slug:subcategoryslug>/', views.product_list, name="product-subcategory"),
   path('product-category/<slug:categoryslug>/<slug:subcategoryslug>/<slug:childsubcategoryslug>/', views.product_list, name="product-childsubcategory"),
   path('product-price-category/<slug:categoryslug>/', views.ProductListView.as_view(), name="filter_by_category"),
   path('product/sort-value', views.product_cat_sort_value, name='product_cat_sort_value'),
   path('product/<slug:slug>/', views.product_details, name="product_detail"),
   path('get-product-data/', views.get_product_data, name='get_product_data'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)