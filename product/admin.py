"""
Register your models here.
"""
from django.contrib import admin
from product.models import Brand, Category, Color, Product, UploadedFile


class BrandAdmin(admin.ModelAdmin):
    """
    list of Brands in Admin panel
    """
    list_display = (
        "id",
        "name",
    )


class ColorAdmin(admin.ModelAdmin):
    """
    list of Colors in Admin panel
    """
    list_display = (
        "id",
        "name",
    )


class CategoryAdmin(admin.ModelAdmin):
    """
    list of Categories in Admin panel
    """
    list_display = (
        "id",
        "name",
    )


class ProductAdmin(admin.ModelAdmin):
    """
    list of Products in Admin panel
    """
    list_display = (
        "id",
        "name",
        "created_at",
        "category",
        "brand",
        "color",
        "size",
        "price",
        "type",
    )
    search_fields = ("name", "category", "brand")


class UploadedFileAdmin(admin.ModelAdmin):
    """
    list of Uploaded file in Admin panel
    """
    list_display = ("created_at", "updated_at", "file", "google_sheet")


admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UploadedFile, UploadedFileAdmin)
