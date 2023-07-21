from django.contrib import admin

from .models import Category,Product,Shop,Seller

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','description','price','amount']
    list_editable = ['price']
    list_per_page = 10

admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Seller)

