from django.urls import path

from product import views

urlpatterns = [
    path("", views.ImportProduct.as_view(), name="data_import"),
    path("product_list/", views.ProductList.as_view(), name="product_list"),
    path("export/xls/", views.ExportExcel.as_view(), name="export_data_xls"),
    path("export/csv/", views.ExportCSV.as_view(), name="export_data_csv"),
]
