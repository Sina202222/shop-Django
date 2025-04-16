# accounts/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views  # وارد کردن ویوهای مربوطه

from .views import (
     SiteSettingsView, ProductListView,
     HomeView,  CustomLoginView, RegisterView,
     AddProductWholesalerView, AddProductSingleView,
     BankCardView,shopping_cart,
     ProductsPurchasedView, ProductSoldView,
     AddToCartView, CartView
   
    #  ProductsSold, SalesManagement, SellerDetails, MyProductsNewView
     # SingleSaler, WholeSaler 
    )


urlpatterns = [
    # مسیرهای مربوط به اپلیکیشن accounts
    
    path("", HomeView.as_view(template_name="home.html"), name="home"),
    
    path('sitesettings/', SiteSettingsView.as_view() , name='sitesettings'),
    
    path('register/', RegisterView.as_view(), name='register'),
    
    
    path('login/', CustomLoginView.as_view(), name='login'),
 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # استفاده از LogoutView پیش‌فرض
    

    
    path('seller/page_seller/single.html/',AddProductSingleView.as_view() , name='single'),
    path('singlee/', ProductListView.as_view(), name='singlee'),  # URL برای نمایش محصولات
    
    path('seller/page_seller/multy',AddProductWholesalerView.as_view() , name='multy'),
    
    path('detils_products_multy/',HomeView.as_view(template_name="detils_products_multy.html") , name='detils_products_multy'),
    path('detils_products_signal/',HomeView.as_view(template_name="detils_products_signal.html") , name='detils_products_signal'),
    
    
    # path('shopping_cart/',shopping_cart , name='shopping_cart'),
    
    
    
    
    path('seller/bankcard/', BankCardView.as_view(), name='bankcard'),
  
    path('user/products_purchased/', ProductsPurchasedView.as_view(), name='products_purchased'),
    path('seller/products_sold/', ProductSoldView.as_view(), name='products_sold'),
    
    
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),  # URL برای نمایش سبد خرید
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)