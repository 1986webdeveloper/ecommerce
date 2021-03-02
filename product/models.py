"""product tables"""
from django.db import models


class TimeStampMixin(models.Model):
    """abstract timestamp table"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampMixin):
    """category table"""
    name = models.CharField(
        "Name", max_length=150, blank=True, null=True, unique=True
    )

    def __str__(self):
        return self.name


class Color(TimeStampMixin):
    """color table"""
    name = models.CharField("Name", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(TimeStampMixin):
    """brand table"""
    name = models.CharField("Name", max_length=150)

    def __str__(self):
        return self.name


class Product(TimeStampMixin):
    """product table"""
    name = models.CharField("Product Name", max_length=150)
    description = models.CharField(
        "Product Description", max_length=250, blank=True, null=True
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name="products", on_delete=models.CASCADE)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    size = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.name}-{self.brand}"


class UploadedFile(TimeStampMixin):
    """uploaded file table"""
    file = models.FileField(upload_to="files/", blank=True, null=True)
    google_sheet = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.file.name}" or f"{self.google_sheet}"
