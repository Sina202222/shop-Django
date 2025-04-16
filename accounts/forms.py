# accounts/forms.py

from django import forms
from .models import ( 
                     SiteSettings,
                     CustomUser, AddProductSingle,
                     AddProductWholesaler, Cart,
                     BankCard, PurchasedProduct,
                     ProductSold
                     )       
from django.utils.translation import gettext_lazy as _  # این خط را اضافه کنید

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinValueValidator


from django.contrib.contenttypes.models import ContentType


# محصولات موجود 
class SiteSettingsForm(forms.ModelForm):
  
    class Meta:
        model = SiteSettings
        fields = ['logo']

    

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, label='نوع کاربر')
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'user_type' ]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # اطمینان حاصل کنید که این خط وجود دارد

    username = forms.CharField(
        label=_("Username"),
        max_length=254,
    )
        
    password = forms.CharField(
        label=_("Password"),
        strip=False,
    )
    
    # اضافه کردن فیلد جدید (اختیاری)
    remember_me = forms.BooleanField(
        required=False,
        label=_("Remember Me"),
        
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # اعتبارسنجی سفارشی (اختیاری)
        if username and password:
            # می‌توانید منطق اعتبارسنجی خود را اینجا اضافه کنید
            pass

        return cleaned_data


# محصولات موجود 
class AddProductWholesalerForm(forms.ModelForm):
    cost = forms.FloatField(
        validators=[MinValueValidator(0)],  # فقط اعداد مثبت
        
    )
    
    class Meta:
        model = AddProductWholesaler
        fields = [ 'name_store', 'category_product', 'name_product', 'numbers', 'features_product', 'description', 'cost', 'image']


# محصولات موجود 
class AddProductSingleForm(forms.ModelForm):
    cost = forms.FloatField(
        validators=[MinValueValidator(0)],  # فقط اعداد مثبت
        
    )
    
    class Meta:
        model = AddProductSingle
        fields = [ 'name_store', 'category_product', 'name_product', 'features_product', 'description', 'cost', 'image']
        

class AddCartForm(forms.ModelForm):
        model= Cart
        fields = ['product_id', 'product_name', 'product_cost', 'quantity', 'created_at']


# مدل جدیدی برای ذخیره شماره کارت‌های بانکی کاربران ایجاد کنید
class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ['card_number', 'card_type', 'expiration_date']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'] = forms.ModelChoiceField(queryset=CustomUser .objects.filter(id=user.id), initial=user)
    
        
# مدلی برای ذخیره اطلاعات محصولات خریداری شده ایجاد کنید 
class PurchasedProductForm(forms.ModelForm):
    class Meta:
        model = PurchasedProduct
        fields = ['user', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن فیلد برای انتخاب نوع محصول
        self.fields['content_type'] = forms.ModelChoiceField(
            queryset=ContentType.objects.filter(model__in=['addproductwholesaler', 'addproductsingle']),
            empty_label="Select Product Type"
        )
        self.fields['object_id'] = forms.IntegerField(label="Product ID")
   
   
   
# مدلی برای ذخیره اطلاعات محصولات فروخته شده ایجاد کنید
class ProductSoldForm(forms.ModelForm):
    class Meta:
        model = ProductSold
        fields = ['quantity']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اضافه کردن فیلد برای انتخاب نوع محصول
        self.fields['content_type'] = forms.ModelChoiceField(
            queryset=ContentType.objects.filter(model__in=['addproductwholesaler', 'addproductsingle']),
            empty_label="Select Product Type"
        )
        self.fields['object_id'] = forms.IntegerField(label="Product ID")