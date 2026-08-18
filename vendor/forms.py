from django import forms
from .models import *

class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=200)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    name=forms.CharField(max_length=100)
    company_name=forms.CharField(max_length=200)
    contact=forms.CharField(max_length=10)
    Role_choices=[
        ("Vendor","Vendor"),
        ("Supplier","Supplier"),
    ]
    role=forms.ChoiceField(choices=Role_choices)
    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        return username

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)

class ProductForm(forms.ModelForm):
    
    class Meta:
        model=Product
        fields=["image","name","category","description","price","unit","minimum_order_quantity","stock_quantity"]

class RFQForm(forms.ModelForm):
    class Meta:
        model=RFQ
        fields=["quantity","description","required_by"]
        widgets = {
            "required_by": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotation

        fields = [
            "delivery_days",
            "valid_until",
            "terms",
        ]

        widgets = {
            "delivery_days": forms.NumberInput(
                attrs={
                    "placeholder": "Enter delivery days",
                    "min": 1,
                }
            ),

            "valid_until": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }