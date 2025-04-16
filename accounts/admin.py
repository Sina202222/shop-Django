from django.contrib import admin
from .models import AddProductWholesaler, AddProductSingle, CustomUser, SiteSettings
# Register your models here.
admin.site.register(AddProductWholesaler) 
admin.site.register(AddProductSingle) 


admin.site.register(CustomUser) 

# admin.site.register(CartView) 



