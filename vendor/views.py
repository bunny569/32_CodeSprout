from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.db import models
def landing(request):
    return render(request,"landingpage.html")
def user_login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]

            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                if user.groups.filter(name="Vendor").exists():
                    return redirect("vendordashboard")
                elif user.groups.filter(name="Supplier").exists():
                    return redirect("supplierdashboard")
                else:
                    form.add_error(
                        None,
                        "Your account does not have a Vendor or Supplier role."
                    )
            else:
                form.add_error(
                    None,"Invalid username or password"
                )
    else:
        form=LoginForm()
    return render(request,"login.html",{"form":form})
def registration(request):
   if request.method=="POST":
       form=RegistrationForm(request.POST)
       if form.is_valid():
           role=form.cleaned_data["role"]
           user=User.objects.create_user(
               username=form.cleaned_data["username"],
               email=form.cleaned_data["email"],
               password=form.cleaned_data["password"],
           )
           if role == "Vendor":
              Vendor.objects.create(
                  user=user,
                  company_name=form.cleaned_data["company_name"],
                  name=form.cleaned_data["name"],
                  contact=form.cleaned_data["contact"],
              )
              vendor_group=Group.objects.get(name="Vendor")
              user.groups.add(vendor_group)
           elif role == "Supplier":
               Supplier.objects.create(
                   user=user,
                   company_name=form.cleaned_data["company_name"],
                   name=form.cleaned_data["name"],
                   contact=form.cleaned_data["contact"],
               )
               supplier_group=Group.objects.get(name="Supplier")
               user.groups.add(supplier_group)
           return redirect("login")
   else:
            form=RegistrationForm()
   return render(request,"registration.html",{
           "form":form})
@login_required
def vendordashboard(request):

    vendor = Vendor.objects.get(user=request.user)

    products = Product.objects.all()

    rfqs = RFQ.objects.filter(
        vendor=vendor
    )

    quotations = Quotation.objects.filter(
        rfq__vendor=vendor
    )

    orders = PurchaseOrder.objects.filter(
        vendor=vendor
    )

    return render(request, "vendordashboard.html", {
        "vendor": vendor,
        "products": products,
        "rfqs": rfqs,
        "quotations": quotations,
        "orders": orders,
    })
@login_required
def supplierdashboard(request):

    supplier = Supplier.objects.get(user=request.user)

    products = Product.objects.filter(
        supplier=supplier
    )

    rfqs = RFQ.objects.filter(
        supplier=supplier
    )

    quotations = Quotation.objects.filter(
        supplier=supplier
    )

    orders = PurchaseOrder.objects.filter(
        supplier=supplier
    )

    pending_rfqs = rfqs.filter(
        status="Pending"
    )

    pending_orders = orders.filter(
        status="Pending"
    )

    return render(request, "supplierdashboard.html", {
        "supplier": supplier,
        "products": products,
        "rfqs": rfqs,
        "quotations": quotations,
        "orders": orders,
        "pending_rfqs": pending_rfqs,
        "pending_orders": pending_orders,
    })

@login_required
def addproduct(request):

    supplier = Supplier.objects.get(user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier
            product.save()

            return redirect("supplierdashboard")

    else:
        form = ProductForm()

    return render(request, "addproduct.html", {"form": form})
@login_required
def productview(request):
    query=request.GET.get("q","")
    products=Product.objects.select_related("supplier").all()

    if query:
        products=products.filter(name__icontains=query)

    return render(request, "products.html", {
        "products": products,
        "query": query,
    })

@login_required
def request_quotation(request,id):
    product=get_object_or_404(Product,id=id)
    vendor=Vendor.objects.get(user=request.user)
    supplier=product.supplier
    if request.method == "POST":
        form=RFQForm(request.POST)
        if form.is_valid():
            rfq=form.save(commit=False)
            rfq.vendor=vendor
            rfq.supplier=supplier
            rfq.product=product

            rfq.save()
            return redirect("productview")
    else:
            form=RFQForm()
    return render(request,"requestquotation.html",{"product":product,"supplier":supplier,"form":form})

@login_required
def supplier_rfqs(request):

    supplier = Supplier.objects.get(user=request.user)

    rfqs = RFQ.objects.filter(
        supplier=supplier
    )

    print("LOGGED SUPPLIER:", supplier)
    print("RFQ COUNT:", rfqs.count())

    for rfq in rfqs:
        print(
            "RFQ:",
            rfq.id,
            "Supplier:",
            rfq.supplier,
            "Status:",
            rfq.status
        )

    return render(request, "supplier_rfq.html", {
        "rfqs": rfqs
    })
@login_required
def submitquotation(request,id):
    supplier=Supplier.objects.get(user=request.user)
    rfq=get_object_or_404(RFQ,id=id)
    if request.method=="POST":
        form=QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)

            quotation.rfq = rfq
            quotation.supplier = supplier

            quotation.quantity = rfq.quantity

            quotation.unit_price = rfq.product.price

            quotation.total_price = (
            quotation.unit_price * quotation.quantity
                     )

            quotation.save()
            rfq.status = "Quoted"
            rfq.save()
            return redirect("supplierrfq")

    else:
        form=QuotationForm()
    return render(request,"submitquotation.html",{"form":form,"rfq":rfq})

@login_required
def vendor_quotations(request):

    vendor = Vendor.objects.get(user=request.user)

    quotations = Quotation.objects.filter(
        rfq__vendor=vendor
    ).select_related(
        "supplier",
        "rfq",
        "rfq__product"
    )

    return render(request, "vendorquotations.html", {
        "quotations": quotations
    })

@login_required
def quotation_action(request, id, action):

    quotation = get_object_or_404(Quotation, id=id)

    vendor = Vendor.objects.get(user=request.user)

    if quotation.rfq.vendor != vendor:
        return redirect("vendorquotations")

    if action == "accept":

        quotation.status = "Accepted"
        quotation.save()

        if not PurchaseOrder.objects.filter(
            quotation=quotation
        ).exists():

            order = PurchaseOrder.objects.create(
                vendor=quotation.rfq.vendor,
                supplier=quotation.supplier,
                quotation=quotation,
                order_date=timezone.now().date(),
                expected_delivery=(
                    timezone.now().date()
                    + timedelta(days=quotation.delivery_days)
                ),
                total_price=quotation.total_price,
                status="Pending"
            )

    elif action == "reject":

        quotation.status = "Rejected"
        quotation.save()
        quotation.rfq.status = "Rejected"
        quotation.rfq.save()

    return redirect("vendorquotations")
@login_required
def vendor_purchase_orders(request):

    vendor = Vendor.objects.get(user=request.user)

    orders = PurchaseOrder.objects.filter(
        vendor=vendor
    )

    return render(request, "vendorpurchaseorders.html", {
        "orders": orders
    })

@login_required
def supplier_purchase_orders(request):

    supplier = Supplier.objects.get(user=request.user)

    orders = PurchaseOrder.objects.filter(
        supplier=supplier
    )

    return render(request, "supplierpurchaseorders.html", {
        "orders": orders
    })
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def inventory(request):

    supplier = Supplier.objects.get(user=request.user)

    products = Product.objects.filter(
        supplier=supplier
    )

    return render(request, "inventory.html", {
        "products": products
    })

@login_required
def update_inventory(request, id):

    supplier = Supplier.objects.get(user=request.user)

    product = get_object_or_404(
        Product,
        id=id,
        supplier=supplier
    )

    if request.method == "POST":

        quantity = request.POST.get("quantity")

        if quantity:
            product.stock_quantity = quantity
            product.save()

        return redirect("inventory")

    return render(request, "updateinventory.html", {
        "product": product
    })
@login_required
def analytics(request):

    supplier = Supplier.objects.get(user=request.user)



    products = Product.objects.filter(
        supplier=supplier
    )

    inventory_labels = []
    inventory_values = []

    for product in products:

        inventory_labels.append(
            product.name
        )

        inventory_values.append(
            float(product.stock_quantity)
        )




    rfqs = RFQ.objects.filter(
        supplier=supplier
    )

    rfq_pending = rfqs.filter(
        status="Pending"
    ).count()

    rfq_quoted = rfqs.filter(
        status="Quoted"
    ).count()

    rfq_accepted = rfqs.filter(
        status="Accepted"
    ).count()

    rfq_rejected = rfqs.filter(
        status="Rejected"
    ).count()

    rfq_expired = rfqs.filter(
        status="Expired"
    ).count()




    orders = PurchaseOrder.objects.filter(
        supplier=supplier
    )

    order_pending = orders.filter(
        status="Pending"
    ).count()

    order_delivered = orders.filter(
        status="Delivered"
    ).count()

    order_cancelled = orders.filter(
        status="Cancelled"
    ).count()



    return render(
        request,
        "analytics.html",
        {

            "inventory_labels": inventory_labels,
            "inventory_values": inventory_values,

            "rfq_pending": rfq_pending,
            "rfq_quoted": rfq_quoted,
            "rfq_accepted": rfq_accepted,
            "rfq_rejected": rfq_rejected,
            "rfq_expired": rfq_expired,

            "order_pending": order_pending,
            "order_delivered": order_delivered,
            "order_cancelled": order_cancelled,

        }
    )
@login_required
def supplier_order_action(request, id, action):

    supplier = Supplier.objects.get(
        user=request.user
    )

    order = get_object_or_404(
        PurchaseOrder,
        id=id,
        supplier=supplier
    )

    if action == "confirm":

        if order.status == "Pending":
            order.status = "Confirmed"
            order.save()

    elif action == "cancel":

        if order.status == "Pending":
            order.status = "Cancelled"
            order.save()

    elif action == "ship":

        if order.status == "Confirmed":
            order.status = "Shipped"
            order.save()

    return redirect("supplierpurchaseorders")

@login_required
def vendor_order_action(request, id, action):

    vendor = Vendor.objects.get(
        user=request.user
    )

    order = get_object_or_404(
        PurchaseOrder,
        id=id,
        vendor=vendor
    )

    if action == "delivered":

        if order.status == "Shipped":

            order.status = "Delivered"
            order.save()

    return redirect("vendorpurchaseorders")
@login_required
def vendor_analytics(request):

    vendor = Vendor.objects.get(user=request.user)

    rfqs = RFQ.objects.filter(vendor=vendor)

    # RFQ counts
    rfq_pending = rfqs.filter(status="Pending").count()
    rfq_quoted = rfqs.filter(status="Quoted").count()
    rfq_accepted = rfqs.filter(status="Accepted").count()
    rfq_rejected = rfqs.filter(status="Rejected").count()
    rfq_expired = rfqs.filter(status="Expired").count()

    # Purchase orders
    orders = PurchaseOrder.objects.filter(vendor=vendor)

    order_pending = orders.filter(status="Pending").count()
    order_confirmed = orders.filter(status="Confirmed").count()
    order_shipped = orders.filter(status="Shipped").count()
    order_delivered = orders.filter(status="Delivered").count()
    order_cancelled = orders.filter(status="Cancelled").count()

    # Spending by supplier
    supplier_ids = orders.values_list(
        "supplier_id",
        flat=True
    ).distinct()

    suppliers = Supplier.objects.filter(
        id__in=supplier_ids
    )

    supplier_names = []
    supplier_spending = []

    for supplier in suppliers:

        total = orders.filter(
            supplier=supplier,
            status="Delivered"
        ).aggregate(
            total=models.Sum("total_price")
        )["total"] or 0

        supplier_names.append(
            supplier.company_name
        )

        supplier_spending.append(
            float(total)
        )

    return render(
        request,
        "vendoranalytics.html",
        {
            "rfq_pending": rfq_pending,
            "rfq_quoted": rfq_quoted,
            "rfq_accepted": rfq_accepted,
            "rfq_rejected": rfq_rejected,
            "rfq_expired": rfq_expired,

            "order_pending": order_pending,
            "order_confirmed": order_confirmed,
            "order_shipped": order_shipped,
            "order_delivered": order_delivered,
            "order_cancelled": order_cancelled,

            "supplier_names": supplier_names,
            "supplier_spending": supplier_spending,
        }
    )
@login_required
def vendor_profile(request):

    vendor = Vendor.objects.get(
        user=request.user
    )

    return render(
        request,
        "vendorprofile.html",
        {
            "vendor": vendor
        }
    )
@login_required
def supplier_profile(request):

    supplier = Supplier.objects.get(
        user=request.user
    )

    return render(
        request,
        "supplierprofile.html",
        {
            "supplier": supplier
        }
    )
@login_required
def edit_vendor_profile(request):

    vendor = Vendor.objects.get(
        user=request.user
    )

    if request.method == "POST":

        vendor.company_name = request.POST.get("company_name")
        vendor.name = request.POST.get("name")
        vendor.contact = request.POST.get("contact")
        vendor.address = request.POST.get("address")
        vendor.industry = request.POST.get("industry")
        vendor.description = request.POST.get("description")

        vendor.save()

        request.user.email = request.POST.get("email")
        request.user.save()

        return redirect("vendorprofile")

    return render(
        request,
        "editvendorprofile.html",
        {
            "vendor": vendor
        }
    )
@login_required
def edit_supplier_profile(request):

    supplier = Supplier.objects.get(
        user=request.user
    )

    if request.method == "POST":

        supplier.company_name = request.POST.get(
            "company_name"
        )

        supplier.name = request.POST.get(
            "name"
        )

        supplier.contact = request.POST.get(
            "contact"
        )

        supplier.address = request.POST.get(
            "address"
        )

        supplier.website = request.POST.get(
            "website"
        )

        supplier.description = request.POST.get(
            "description"
        )

        supplier.save()

        request.user.email = request.POST.get(
            "email"
        )

        request.user.save()

        return redirect("supplierprofile")

    return render(
        request,
        "editsupplierprofile.html",
        {
            "supplier": supplier
        }
    )