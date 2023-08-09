from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced,
    BCart, 
    Designer,
    DesignerPlaced,
    TempDesignerPlaced,
    DesignerWorks,
    Profile,
)
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "locality", "city", "zipcode", "state"]


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "selling_price", "discounted_price", "description", "brand", "category", "product_image"]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]

@admin.register(BCart)
class BCartModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "customer", "customer_info", "product_info", "product", "quantity", "ordered_date", "status"]


    def customer_info(self,obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}', link, obj.customer.name)
    
    def product_info(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}', link, obj.product.title)
    

@admin.register(Designer)
class DesignerModelAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "designer_code", "full_name", "email", "phone", "work_exp", "address", "zipcode", "state", "designer_image"]
    

@admin.register(DesignerPlaced)
class DesignerPlacedModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "customer", "designer", "ordered_date", "status"]


@admin.register(TempDesignerPlaced)
class TempDesignerPlacedModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "designer"]


@admin.register(DesignerWorks)
class DesignerWorksModelAdmin(admin.ModelAdmin):
    list_display = ["id", "designer", "works_img", "descriptions"]

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "token", "verify"]