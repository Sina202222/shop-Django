# accounts/models.py
from django.shortcuts import render, redirect

from django.db import models
from django.contrib.auth.models import AbstractUser   
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



# @receiver(post_migrate)
# def create_default_settings(sender, **kwargs):
#     if not SiteSettings.objects.exists():
#         SiteSettings.objects.create(site_name='shop')

class SiteSettings(models.Model):
    # site_name = models.CharField(max_length=100, default='نام سایت')
    logo = models.ImageField(upload_to='images/logo')

    def __str__(self):
        return "logo"
    
    
class CustomUser (AbstractUser ):
    USER_TYPE_CHOICES = [
        ('buyer', 'خریدار'),
        ('product_wholesaler', 'عمده فروش'),
        ('product_single', 'تک فروش'),
    ]
    user_type = models.CharField(max_length=24, choices=USER_TYPE_CHOICES, verbose_name='نوع کاربر')

    def __str__(self):
        return self.username

    


class AddProductWholesaler(models.Model):  
    
    name_store = models.CharField(max_length=100)  # نام فروشگاه 
    category_product = models.CharField(max_length=225)  # دسته بندی
    name_product = models.CharField(max_length=100)  # نام محصول
    numbers = models.IntegerField()   # تعداد موجود در یک بسته 
    
    features_product = models.TextField()  # ویژگی های محصول
    description = models.TextField()  # توضیحات در مورد محصول
    cost = models.DecimalField(max_digits=10, decimal_places=2)   # هزینه محصول
    image = models.ImageField(upload_to='images/product_wholesaler/')  # عکس از محصول 
    
    date = models.DateField(default=timezone.now)  # تاریخ ایجاد     
    
    def __str__(self):
        return f"{self.name_product} by {self.name_store}"



class AddProductSingle(models.Model):  
    
    name_store = models.CharField(max_length=100)  # نام فروشگاه 
    category_product = models.CharField(max_length=225)  # دسته بندی
    name_product = models.CharField(max_length=100)  # نام محصول
    
    features_product = models.TextField()  # ویژگی های محصول
    description = models.TextField()  # توضیحات در مورد محصول
    cost = models.DecimalField(max_digits=10, decimal_places=2)   # هزینه محصول
    image = models.ImageField(upload_to='images/product_single/')  # عکس از محصول 
    
    date = models.DateField(default=timezone.now)  # تاریخ ایجاد     
    
    def __str__(self):
        return f"{self.name_product} by {self.name_store}"



class Cart(models.Model):
    
    product_id = models.IntegerField()                                  # شناسه محصول
    product_name = models.CharField(max_length=255)  # نام محصول
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)  # قیمت محصول
    quantity = models.IntegerField(default=1)                            # تعداد محصول
    created_at = models.DateTimeField(auto_now_add=True)                    # تاریخ ایجاد
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} pcs"


class BankCard(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='bank_cards')  # ارتباط با کاربر
    card_number = models.CharField(max_length=16, validators=[RegexValidator(r'^\d{16}$')])  # شماره کارت بانکی
    card_type = models.CharField(max_length=10, choices=[
        ('Visa', 'ویزا'),
        ('MasterCard', 'مسترکارت'),
        ('Other', 'سایر')
    ])  # نوع کارت
    expiration_date = models.DateField()  # تاریخ انقضا
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد

    class Meta:
        verbose_name = "Bank Card"
        verbose_name_plural = "Bank Cards"

    def __str__(self):
        return f"{self.card_type} ending with {self.card_number[-4:]}"



class PurchasedProduct(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='purchased_products')  # ارتباط با کاربر
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # نوع محصول
    object_id = models.PositiveIntegerField()  # شناسه محصول
    product = GenericForeignKey('content_type', 'object_id')  # ارتباط با محصول
    quantity = models.PositiveIntegerField()  # تعداد خریداری شده

    class Meta:
        verbose_name = "Purchased Product"
        verbose_name_plural = "Purchased Products"

    def __str__(self):
        return f"{self.quantity} of {self.product.name_product} purchased by {self.user.username}"



class ProductSold(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='sold_products')  # کاربر خریدار
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # نوع محصول
    object_id = models.PositiveIntegerField()  # شناسه محصول
    product = GenericForeignKey('content_type', 'object_id')  # ارتباط با محصول
    quantity = models.PositiveIntegerField()  # تعداد فروخته شده

    class Meta:
        verbose_name = "Sold Product"
        verbose_name_plural = "Sold Products"
        
    def __str__(self):
        return f"{self.quantity} of {self.product.name_product} sold "

   