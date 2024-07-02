from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
   path('Dashboard', views.Dashboard, name="Dashboard"),
   path('product-adding', views.product_adding, name="product-adding"),
   # path('product-admin', views.product_admin, name="product-admin"),   
   path('get-subcategories', views.get_subcategories, name='get-subcategories'),
   path('get-brand', views.get_brand, name='get-brand'),
   path('Attribute-values', views.Attr_values, name='Attribute-values'),
   # Add new Category & subcategory & Brand URLS
   path('create/category/', views.create_category, name='create_category'),
   path('create/subcategory/', views.create_subcategory, name='create_subcategory'),
   path('create/brand/', views.create_brand, name='create_brand'),
   path('category-admin', views.category_admin, name="category-admin"),
   path('subcategory-admin', views.subcategory_admin, name="subcategory-admin"),
   path('brand-admin', views.brand_admin, name="brand-admin"),
   path('export-xls', views.export_to_xls, name="export-xls"),
   path('download-sample-xls', views.download_sample_xls, name="download-sample-xls"),
   path('import-product', views.import_product, name="import-product"),
   path('update-product', views.update_product, name="update-product"),
   path('get-attribute', views.get_attribute, name="get-attribute"),
   path('filter-data', views.filter_data, name="filter-data"),
   path('upsell-selection', views.upsell_selection, name='upsell-selection'),
   
   path('sales/order', views.order_page, name="admin-order"),
#    path('order-details', views.order_details, name="order-details"),
   path('order-details/<str:order_id>/', views.order_details, name="order-details"),
   path('order-status-update', views.order_status_update, name='order-status-update'),
   path('order-filter-data', views.order_filter_data, name='order-filter-data'),

   path('sales/order-create-user', views.back_order_user, name='sales/order-create-user'),
   path('sales/back-order-form/<int:id>/', views.back_order_form, name='sales/back-order-form'),
   path('order_product_selection', views.order_product_selection, name="order_product_selection"),
   path('back_order', views.back_order, name="back_order"),

   path('order_data_get', views.order_data_get, name='order_data_get'),
   path('sales/order-filter/<str:category>/', views.order_data_get, name='sales/order-filter'),
   path('product_data_get', views.product_data_get, name='product_data_get'),
   path('product-filter/<str:category>/', views.product_data_get, name='product-filter'),
   path('product-filter-data', views.product_filter_data, name='product-filter-data'),
   path('product-filter-data/<str:category>/', views.product_filter_data, name='product-filter-data'),

   # path('customer', views.customer, name="customer"),
   path('customer', CustomerListView.as_view(), name='customer'),
   path('customer/new', views.custom_user, name='customer_new'),
   path('customer-details/<int:id>', views.customer_details, name='customer-details'),
   path('Customer/<int:customerId>/delete/', views.delete_customer, name='delete_customer'),
   path('export-user-data/', views.export_user_data_as_csv, name='export_user_data'),
   path('update-billing-info/<int:id>/', views.updatebilling, name='updatebilling'),

   path('coupon', views.coupon, name='coupon'),
   path('add-coupon', views.addcoupon, name='add-coupon'),
   path('coupon-useage', views.couponUseage, name='couponUseage'),
   path('update_coupon', views.update_coupon, name='update_coupon'),
   path('coupons/<int:coupon_id>/delete/', views.delete_coupon, name='delete_coupon'),

   path('brand-admin/<int:brand_id>', views.brand_admin, name='brand-admin'),
   path('brand/<int:brand_id>/delete/', views.delete_brand, name='delete_brand'),


   path('subcategory/<int:subcategory_id>/delete/', views.delete_subcategory, name='delete_subcategory'),
   path('subcategory-admin/<int:subcategory_id>', views.subcategory_admin, name='subcategory-admin'),

   path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
   path('category-admin/<int:category_id>', views.category_admin, name='category-admin'),


   path('product-update/<int:product_id>/', views.product_update, name='product_update'),
   path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),

   path('remove-image/<int:image_id>/', views.remove_image, name='remove_image'),

   path('order-replace-page', views.order_replacement_page, name='order-replace-page'),
   path('order-replace-details-page/<str:order_id>/', views.order_replacement_details, name='order-replace-details-page'),
   path('order-replace-status-update', views.replace_order_status_update, name='order-replace-status-update'),
   path('collect_person_asign', views.collect_person_asign, name='collect_person_asign'),
   path('delivery_person_asign', views.delivery_person_asign, name='delivery_person_asign'),

   # path('attribute-admin', views.attribute_admin, name='attribute-admin'),
   path('attribute-admin', AttributeListView.as_view(), name='attribute-admin'),

   path('add_new_attribute', views.add_new_attribute, name='add_new_attribute'),
   path('update_attribute', views.update_attribute, name='update_attribute'),
   path('Attribute/<int:attribute_id>/delete/', views.delete_attribute, name='delete_attribute'),


   path('add_new_attribute_value', views.add_new_attribute_value, name='add_new_attribute_value'),
   path('update_attribute_value', views.update_attribute_value, name='update_attribute_value'),
   path('Attribute-Value/<int:attribute_value_id>/delete/', views.delete_attribute_value, name='delete_attribute_value'),

   path('export_out_of_stock_to_excel', views.export_out_of_stock_to_excel, name='export_out_of_stock_to_excel'),
   path('import-stock-data', views.import_stock_from_csv, name='import-stock-data'),
   path('import-attribute-from-csv', views.import_attribute_from_csv, name='import-attribute-from-csv'),
   path('export-attribute-values', views.export_attribute_values, name='export_attribute_values'),

   path('products/', ProductListView.as_view(), name='product-list'),
   

# banners
#    path('mainbanners', views.mainpage_Banner, name='mainbanner'),
#    path('mainbanners/<int:banner_id>/', views.mainpage_Banner, name='mainbanner'),
#    path('delete_buypromo/<int:banner_id>/delete/', views.delete_buypromo, name='delete_buypromo'),

   
   path('Buy-Promo-Banner', views.mainpage_Banner, name='Buy-Promo-Banner'),
   path('Buy-Promo-Banner/<int:banner_id>/', views.mainpage_Banner, name='Buy-Promo-Banner'),
   path('mainpage_Banner/<int:banner_id>/delete/', views.delete_buypromo, name='delete_buypromo'),


#    path('trendingbanner', views.Trending_Banner, name='trendingbanner'),
#    path('trendingbanner/<int:banner_id>/', views.Trending_Banner, name='trendingbanner'),
#    path('trendingbanner/<int:banner_id>/delete/', views.delete_buypromo, name='delete_buypromo'),

   path('pricebanners', views.Price_Banner, name='pricebanner'),
   path('pricebanners/<int:banner_id>/', views.Price_Banner, name='pricebanner'),
   path('deletepricebanner/<int:banner_id>/delete/', views.delete_pricebanner, name='delete_offerbanner'),

   path('footerbanners', views.footer_Banner, name='footerbanner'),
   path('footerbanners/<int:banner_id>/', views.footer_Banner, name='footerbanner'),
   path('footerbanners/<int:banner_id>/delete/', views.delete_footerbanner, name='delete_footerbanner'),

#    path('categorybanner', views.category_Banner, name='categorybanner'),
#    path('categorybanner/<int:banner_id>/', views.category_Banner, name='categorybanner'),
#    path('categorybanner/<int:banner_id>/delete/', views.delete_categorybanner, name='delete_categorybanner'),

   path('group', views.create_group, name='group'),
#    path('group/<int:group_id>/', views.create_group, name='group'),
   path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
   path('group/<int:group_id>/change/', views.edit_group, name='group-edit'),

   path('user/permissions', views.assign_permissions, name='permissions'),
   path('user/permissions/<int:user_id>/change/', views.change_permissions, name='permissions-change'),

   path('delivery-person', views.delivery_person, name='delivery_person'),
   path('delivery-person/<int:delivery_person_id>', views.delivery_person, name='delivery_person'),
   path('delivery-person/<int:delivery_person_id>/delete/', views.delete_delivery_person, name='delete_delivery_person'),

   path('replacement-collect-person', views.replacement_person, name='replacement_person'),
   path('replacement-collect-person/<int:replace_collect_person_id>', views.replacement_person, name='replacement_person'),
   path('replacement-collect-person/<int:replace_collect_person_id>/delete/', views.delete_replacement_person, name='delete_replacement_person'),

   path('invoice-report', views.generate_invoice_report, name='generate_invoice_report'),
   path('export-invoice-csv', views.export_invoice_csv, name='export_invoice_csv'),

   path('generate-order-report', views.generate_order_report, name='generate_order_report'),
   path('export-order-csv', views.export_order_csv, name='export_order_csv'),

   path('generate-order-shipping-report', views.generate_order_shipping_report, name='generate_order_shipping_report'),
   path('export-order-shipping-csv', views.export_order_shipping_csv, name='export_order_shipping_csv'),

   path('generate-coupon-report', views.generate_coupon_report, name='generate_coupon_report'),
   path('export-coupon-csv', views.export_coupon_csv, name='export_coupon_csv'),



   path('tags_product/', views.tags_product, name='tags_product'),
   path('tags_product/<int:tags_id>/', views.tags_product, name='tags_product'),
   path('tags_product/<int:tags_id>/delete', views.tags_product, name='tags_product'),

#    path('robots', views.robots_txt_view, name= 'robots'),  # robots.txt view
#    path('google-tag-manager', views.google_tag_manager_view, name= 'google_tag_manager'),  # Google Tag Manager view
#    path('google-tag-manager/<int:gtm_id>', views.google_tag_manager_view, name= 'google_tag_manager'),  # Google Tag Manager view

#    path('robots/delete/<int:robots_id>/', robots_txt_delete, name='robots_delete'),
#    path('google-tag-manager/<int:gtm_id>/delete/', google_tag_manager_delete, name='google_tag_manager_delete'),

#    path('offer-admin', views.offer_admin, name="offer-admin"),
#    path('offer-update/<int:id>', views.offer_update_view, name="offer-update"),
#    path('offer-admin/<int:offer_id>/delete/', views.delete_offer, name='delete_offer'),
 



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)