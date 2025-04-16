# accounts/views.py


from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin  
# from django.contrib.auth.models import User

from django.views import View 
from django.contrib.auth.views import LoginView 

from django.contrib.auth import logout
from django.contrib import messages

from django.urls import reverse_lazy

from .models import (
            SiteSettings, CustomUser, 
            AddProductSingle, AddProductWholesaler,
            Cart, BankCard,
            PurchasedProduct, ProductSold,
            AddProductSingle
            
            )
from .forms import( 
                    SiteSettingsForm,
                    CustomUserCreationForm, LoginForm, 
                    AddProductSingleForm, AddProductWholesalerForm,
                    BankCardForm, PurchasedProductForm,
                    ProductSoldForm,
                    )

from django.core.exceptions import ValidationError
from django.db import IntegrityError

import logging




class SiteSettingsView(CreateView):
    model= SiteSettings
    form_class= SiteSettingsForm
    template_name= 'admin/sitesettings.html'
   
    def get_success_url(self):
        return reverse_lazy('sitesettings')  # یا هر URL دیگری که می‌خواهید


def upload_logo(request):
    if request.method == 'POST':
        logo = request.FILES.get('logo')  # دریافت فایل لوگو
        site_settings = SiteSettings.objects.get_or_create(id=1)  # فرض بر این است که فقط یک رکورد داریم
        site_settings.logo = logo
        site_settings.save()  # ذخیره تغییرات در پایگاه داده
        return redirect('upload_logo')  # به URL موفقیت‌آمیز هدایت کنید
    return render(request, 'admin/adminn.html')  # نام تمپلیت خود را وارد کنید

class HomeView(TemplateView):
 
    template_name= 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_single'] = AddProductSingle.objects.all()
        context['products_wholesaler'] = AddProductWholesaler.objects.all()
        context['user_type'] = self.request.user.user_type if self.request.user.is_authenticated else None
       
        return context
 

# class AdminnView(TemplateView):
#     model= SiteSettings
#     template_name= 'admin/adminn.html'
   
#     def get_success_url(self):
#         return reverse_lazy('adminn')  # یا هر URL دیگری که می‌خواهید
  
    
# # فرم ثبت نام   
class RegisterView(CreateView):
    model = CustomUser 
    form_class =  CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # آدرس صفحه ورود

    def form_valid(self, form):
        messages.success(self.request, 'ثبت‌نام با موفقیت انجام شد!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً اطلاعات را به درستی وارد کنید.')
        return super().form_invalid(form)


class CustomLoginView(LoginView , TemplateView):
    form_class = LoginForm
    template_name = 'registration/login.html' 
 

class LogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)  # خروج کاربر
        return redirect('home')  # هدایت به صفحه اصلی



logger = logging.getLogger(__name__)


class BaseProductView(CreateView):
    def form_valid(self, form):
        try:
            product = form.save(commit=False)  # ایجاد شیء بدون ذخیره‌سازی
            product.save()  # ذخیره‌سازی
            return super().form_valid(form)  # هدایت به URL موفقیت
        except ValidationError as e:
            form.add_error(None, 'خطا: داده‌ها نمی‌توانند ذخیره شوند.')
            return self.form_invalid(form)  # در صورت خطا، فرم نامعتبر را برگردانید
        except IntegrityError as e:
            form.add_error(None, 'خطا: یکپارچگی داده‌ها نقض شده است.')
            return self.form_invalid(form)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            form.add_error(None, 'خطای غیرمنتظره.')
            return self.form_invalid(form)  # در صورت خطا، فرم نامعتبر را برگردانید
        

class AddProductSingleView(BaseProductView):
    model= AddProductSingle 
    form_class= AddProductSingleForm
    template_name= 'seller/page_seller/single.html'
   
    def get_success_url(self):
        return reverse_lazy('single')  # یا هر URL دیگری که می‌خواهید
    
class ProductListView(View):
    template_name = 'seller/page_seller/single.html'

    def get(self, request, *args, **kwargs):
        products_single = AddProductSingle.objects.all()  # یا هر فیلتر دیگری که نیاز دارید
        return render(request, self.template_name, {'products_single': products_single})    
    


class AddProductWholesalerView(BaseProductView):
    model= AddProductWholesaler
    form_class= AddProductWholesalerForm
    template_name= 'seller/page_seller/multy.html'
    
    def get_success_url(self):
        return reverse_lazy('multy')  # یا هر URL دیگری که می‌خواهید


def shopping_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_cost = request.POST.get('product_cost')

        # بررسی اینکه آیا product_id خالی است
        if not product_id:
            # می‌توانید یک پیام خطا به کاربر نمایش دهید
                return render(request, 'shopping_cart.html', {'error': 'محصول انتخاب نشده است.'})

        # اینجا می‌توانید اطلاعات محصول را به سبد خرید اضافه کنید
        # به عنوان مثال:
        cart_item = Cart(product_id=product_id, product_name=product_name, product_cost=product_cost)
        cart_item.save()

        return redirect('shopping_cart')  # به صفحه سبد خرید بروید

    cart_items = Cart.objects.all()  # دریافت تمام موارد سبد خرید
    # بقیه کدهای ویو برای نمایش سبد خرید
    return render(request, 'shopping_cart.html', {'cart_items': cart_items})


# شماره کارت جدید 
class BankCardView(CreateView):
    model = BankCard
    form_class = BankCardForm
    template_name = 'seller/bankcard.html' 
    success_url = reverse_lazy('bankcard')  

 
# محصولات خریداری شده 
class ProductsPurchasedView(CreateView):
    model = PurchasedProduct
    form_class = PurchasedProductForm
    template_name = 'user/products_purchased.html' 
    success_url = reverse_lazy('products_purchased')  
 
# محصولات فروخته شده 
class ProductSoldView(CreateView):
    model = ProductSold
    form_class = ProductSoldForm
    template_name = 'seller/products_sold.html' 
    success_url = reverse_lazy('products_sold') 
    
    from django.http import HttpResponse
from .models import AddProductSingle

def add_to_cart(request, product_id):
    product = AddProductSingle.objects.get(id=product_id)  # دریافت محصول بر اساس ID
    cart = request.session.get('cart', {})  # دریافت سبد خرید از سشن

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # افزایش تعداد محصول در سبد خرید
    else:
        cart[str(product_id)] = 1  # افزودن محصول به سبد خرید

    request.session['cart'] = cart  # ذخیره سبد خرید در سشن
    return redirect('cart_view')  # هدایت به صفحه سبد خرید 
 
class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(AddProductSingle, id=product_id)  # دریافت محصول بر اساس ID
        cart = request.session.get('cart', {})  # دریافت سبد خرید از سشن

        if str(product_id) in cart:
            cart[str(product_id)] += 1  # افزایش تعداد محصول در سبد خرید
        else:
            cart[str(product_id)] = 1  # افزودن محصول به سبد خرید

        request.session['cart'] = cart  # ذخیره سبد خرید در سشن
        return redirect('cart_view')  # هدایت به صفحه سبد خرید
 
class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = AddProductSingle.objects.filter(id__in=cart.keys())  # دریافت محصولات موجود در سبد خرید
        return render(request, 'cart/cart.html', {'products': products, 'cart': cart}) 

# # مدیریت فروش 
# class SalesManagementView(CreateView):
#     model = MyProducts
#     form_class = MyProductsForm
#     template_name = 'seller/sales_management.html' 
#     success_url = reverse_lazy('sales_management') 
 


# class SingleSaler():  
#     template_name = 'seller/single_saler.html' 
#     success_url = reverse_lazy('home') 
 

# class WholeSaler():   
#     template_name = 'seller/whole_saler.html' 
#     success_url = reverse_lazy('home')  
 