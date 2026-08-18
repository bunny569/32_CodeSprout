from django.contrib import admin
from .models import *


admin.site.register(Vendor)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(RFQ)
admin.site.register(Quotation)
admin.site.register(PurchaseOrder)
admin.site.register(Inventory)