
from django.contrib import admin
from django.urls import path,include
# from django.contrib.auth.decorators import login_required
# from .views import MyPasswordChangeView, MyPasswordSetView
from django.conf.urls.static import static
from django.conf import settings



# shop/urls.py



urlpatterns = [
    path('admin/', admin.site.urls),   
    
    path('', include('accounts.urls')),  # اضافه کردن accounts

    
    # path('accounts/', include('allauth.urls')),  # اگر از django-allauth استفاده می‌کنید
    
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
