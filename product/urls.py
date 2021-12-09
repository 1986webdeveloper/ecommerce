from django.urls import path
from product import views

app_name = "product"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    path("import/", views.ImportProductView.as_view(), name="import"),
    path("export/xls/", views.ExportExcelView.as_view(), name="export-xls"),
    path("export/csv/", views.ExportCSVView.as_view(), name="export-csv"),
]
