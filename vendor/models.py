from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vendor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)
    address=models.TextField()
    industry=models.CharField(max_length=200)
    description=models.TextField(blank=True)

    def __str__(self):
      return self.company_name

class Supplier(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   company_name=models.CharField(max_length=200)
   name=models.CharField(max_length=100)
   contact=models.CharField(max_length=10)
   address=models.TextField()
   description=models.TextField(blank=True)
   website=models.URLField(blank=True)
   rating=models.FloatField(default=0.0)
   images=models.ImageField(upload_to="supplier_images/",blank=True,null=True)
   status_choices=[
      ("Active","Active"),
      ("Pending","Pending"),
      ("Inactive","Inactive"),

   ]
   status=models.CharField(max_length=20,choices=status_choices,default="Pending")

   def __str__(self):
      return self.company_name

class Product(models.Model):
   supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE,related_name="products")
   name=models.CharField(max_length=100)
   category=models.CharField(max_length=100)
   description=models.TextField(blank=True)
   unit=models.CharField(max_length=10)
   price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
   minimum_order_quantity=models.PositiveIntegerField()
   stock_quantity = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0
          )
   image=models.ImageField(upload_to="productimages/",default=None)

   def __str__(self):
      return self.name

class RFQ(models.Model):
   vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
   supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity=models.IntegerField()
   description=models.TextField(blank=True)
   required_by=models.DateField()
   created_at=models.DateTimeField(default=timezone.now)
   status_choices=[
      ("Pending","Pending"),
      ("Quoted","Quoted"),
      ("Accepted","Accepted"),
     ( "Rejected","Rejected"),
      ("Expired","Expired"),
   ]
   status=models.CharField(max_length=20,choices=status_choices,default="Pending")

   def __str__(self):
      return str(self.product)
   
class Quotation(models.Model):
   rfq=models.ForeignKey(RFQ,on_delete=models.CASCADE,related_name="quotations")
   supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
   quantity=models.IntegerField()
   unit_price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
   total_price=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
   delivery_days=models.PositiveIntegerField()
   valid_until=models.DateField()
   terms=models.TextField(blank=True)
   status_choices=[
      ("Pending","Pending"),
      ("Accepted","Accepted"),
     ( "Rejected","Rejected"),
   ]
   status=models.CharField(max_length=20,choices=status_choices,default="Pending")
   created_at=models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.supplier.company_name

class PurchaseOrder(models.Model):
   vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
   supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
   quotation=models.ForeignKey(Quotation,on_delete=models.CASCADE)
   order_date=models.DateField()
   expected_delivery=models.DateField()
   total_price=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
   status_choices=[
      ("Pending","Pending"),
      ("Confirmed","Confirmed"),
      ("Shipped","Shipped"),
      ("Delivered","Delivered"),
     ( "Cancelled","Cancelled"),
   ]
   status=models.CharField(max_length=20,choices=status_choices,default="Pending")

   def __str__(self):
      return self.vendor.company_name

class Inventory(models.Model):
   vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField(default=0)
   reorder_level=models.IntegerField()
   last_updated=models.DateTimeField(default=timezone.now)

   def __str__(self):
      return self.product.name
