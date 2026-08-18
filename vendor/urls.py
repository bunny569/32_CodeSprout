from django.contrib import admin
from django.urls import path
from vendor import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landing,name="landingpage"),
    path('login/',views.user_login,name="login"),
    path('register/',views.registration ,name="registration"),
    path('vendordashboard/',views.vendordashboard,name="vendordashboard"),
    path('supplierdashboard/',views.supplierdashboard,name="supplierdashboard"),
    path('addproduct/',views.addproduct,name="addproduct"),
    path('productview/',views.productview,name="productview"),
    path('requestquotation/<int:id>',views.request_quotation,name="requestquotation"),
    path('supplierrfq/',views.supplier_rfqs,name="supplierrfq"),
    path('submitquotation/<int:id>/',views.submitquotation,name="submitquotation"),
    path('vendorquotation/',views.vendor_quotations,name="vendorquotations"),
    path('quotation_action/<int:id>/<str:action>/',views.quotation_action,name="quotation_action"),
    path("vendorpurchaseorders/",views.vendor_purchase_orders,name="vendorpurchaseorders"),
    path("supplierpurchaseorders/",views.supplier_purchase_orders,name="supplierpurchaseorders"),
    path("inventory/",views.inventory,name="inventory"),
    path("updateinventory/<int:id>/",views.update_inventory,name="updateinventory"),
    path("analytics/",views.analytics,name="analytics"),
    path("supplierorderaction/<int:id>/<str:action>/",views.supplier_order_action,name="supplierorderaction"),
    path("vendororderaction/<int:id>/<str:action>/",views.vendor_order_action,name="vendororderaction"),
    path("vendoranalytics/",views.vendor_analytics,name="vendoranalytics"),
    path("vendorprofile/",views.vendor_profile,name="vendorprofile"),
    path("supplierprofile/",views.supplier_profile,name="supplierprofile"),
    path("editvendorprofile/",views.edit_vendor_profile,name="editvendorprofile"),
    path("editsupplierprofile/",views.edit_supplier_profile,name="editsupplierprofile"),
    path('logout/',views.user_logout,name="logout"),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
