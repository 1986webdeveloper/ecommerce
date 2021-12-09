import csv
import re

import pandas as pd
import xlwt
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView

from product.forms import UploadFileForm
from product.google_api import GoogleSheet
from product.models import Brand, Category, Color, Product, UploadedFile


class ImportProductView(FormView):
    """
    Import products
    either user can pass link of google sheet or file
    file can be a xls or csv
    the data from sheet/file store in database

    file/google-sheet should have first record/header as following (order doesn't matter):
        1. product_name
        2. description
        3. category
        4. brand
        5. color
        6. price - accept two digit after decimal point
        7. size
        8. type
    """

    form_class = UploadFileForm
    template_name = "product/landing.html"
    success_url = "/"
    success_message = ""

    def form_valid(self, form):
        file = form.cleaned_data["file"]
        url = form.cleaned_data["url"]

        if file:
            uploaded_file = UploadedFile.objects.create(file=file)  #
            records = []
            if uploaded_file.file.name.endswith(".csv"):
                records = pd.read_csv(uploaded_file.file).to_dict("records")
            if uploaded_file.file.name.endswith(".xlsx"):
                records = pd.read_excel(uploaded_file.file).to_dict("records")
            self.store_products(records)
            self.success_message = "File successfully Uploaded."

        if url:
            sheet_id = re.search(
                r"https://docs.google.com/spreadsheets/d/([-\w]+)/", url
            ).group(1)
            UploadedFile.objects.create(google_sheet=url)
            records = GoogleSheet.read(sheet_id=sheet_id)
            self.store_products(records)
            self.success_message = "Google sheet Data is successfully imported."
        return super(ImportProductView, self).form_valid(form)

    @staticmethod
    def store_products(records=[]):
        """
        store records in to database
        """
        for record in records:
            try:
                cat, _ = Category.objects.get_or_create(
                    category=record.get("category").capitalize()
                )
                brand, _ = Brand.objects.get_or_create(
                    brand=record.get("brand").capitalize()
                )
                colour, _ = Color.objects.get_or_create(
                    color=record.get("color").capitalize()
                )
                Product.objects.get_or_create(
                    product_name=record.get("product_name"),
                    description=record.get("description"),
                    category=cat,
                    brand=brand,
                    color=colour,
                    price=record.get("price"),
                    size=record.get("size"),
                    type=record.get("type"),
                )
            except Exception as e:
                print(e)


class ProductListView(ListView):
    """
    Product list view
    """

    template_name = "product/list.html"
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.all()


class ExportExcelView(View):
    """
    Export the data of products into Excel file.
    """

    def get(self, request):
        """ This function will export the db data to excel file. """
        response = HttpResponse(content_type="application/ms-excel")

        response[
            "Content-Disposition"
        ] = 'attachment; filename="new_export_data.xls"'  # Set file name ..

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Sheet1")  # this will make the sheet named Sheet1
        row_num = 0  # Sheet header, first row

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [
            "Product Name",
            "Description",
            "Category",
            "Brand",
            "Color",
            "Price",
            "Size",
            "Type",
        ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        # Getting data from the db
        rows = Product.objects.all().values_list(
            "product_name",
            "description",
            "category__category",
            "brand__brand",
            "color__color",
            "price",
            "size",
            "type",
        )

        try:
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
        except Exception as e:
            print(e)
        wb.save(response)
        return response


class ExportCSVView(View):
    """
    Export the data of products into csv file.
    """

    def get(self, request):
        """ This function will export the data to the csv file. """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="new_export_data.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Product Name",
                "Description",
                "Category",
                "Brand",
                "Color",
                "Price",
                "Size",
                "Type",
            ]
        )

        # getting data from the db
        rows = Product.objects.all().values_list(
            "product_name",
            "description",
            "category__category",
            "brand__brand",
            "color__color",
            "price",
            "size",
            "type",
        )
        for row in rows:
            writer.writerow(row)

        return response
