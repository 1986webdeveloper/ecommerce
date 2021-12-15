"""product business logic module"""
import csv
import re

import pandas as pd
import xlwt
from ajax_datatable.views import AjaxDatatableView
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView
from pandas.errors import EmptyDataError

from product.forms import UploadFileForm
from product.google_api import read_gsheet
from product.models import Brand, Category, Color, Product, UploadedFile


class ImportProductView(FormView):
    """
    Import products
    either user can pass link of google sheet or file
    file can be a xls or csv
    the data from sheet/file store in database

    file/google-sheet should have first record/header as following (order doesn't matter):
        1. Product Name
        2. Description
        3. Category
        4. Brand
        5. Color
        6. Price - accept two digit after decimal point
        7. Size
        8. Type
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
                try:
                    records = pd.read_csv(uploaded_file.file).to_dict("records")
                except EmptyDataError as error:
                    print(error)
            if uploaded_file.file.name.endswith(".xlsx"):
                try:
                    records = pd.read_excel(uploaded_file.file).to_dict("records")
                except EmptyDataError as error:
                    print(error)
            self.store_products(records)
            self.success_message = "File successfully Uploaded."

        if url:
            sheet_id = re.search(
                r"https://docs.google.com/spreadsheets/d/([-\w]+)/", url
            ).group(1)
            UploadedFile.objects.create(google_sheet=url)
            records = read_gsheet(sheet_id=sheet_id)
            self.store_products(records)
            self.success_message = "Google sheet Data is successfully imported."
        return super().form_valid(form)

    @staticmethod
    def store_products(records):
        """
        store records in to database
        """
        for record in records:
            try:
                cat, _ = Category.objects.get_or_create(
                    name=record.get("Category").capitalize()
                )
                brand, _ = Brand.objects.get_or_create(
                    name=record.get("Brand").capitalize()
                )
                colour, _ = Color.objects.get_or_create(
                    name=record.get("Color").capitalize()
                )
                price = record.get("Price")
                if not price.replace('.', '', 1).isdigit():
                    continue
                Product.objects.get_or_create(
                    name=record.get("Product Name"),
                    description=record.get("Description"),
                    category=cat,
                    brand=brand,
                    color=colour,
                    price=round(float(price), 2),
                    size=record.get("Size"),
                    type=record.get("Type"),
                )
            except (TypeError, AttributeError, ValueError) as error:
                print(error)


class ProductListView(ListView):
    """
    Product list view
    """

    template_name = "product/list.html"
    paginate_by = 5
    queryset = Product.objects.all().order_by('-id')


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

        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("Sheet1")  # this will make the sheet named Sheet1
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

        for col_num, _ in enumerate(columns):
            worksheet.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        # Getting data from the db
        rows = Product.objects.all().values_list(
            "name",
            "description",
            "category__name",
            "brand__name",
            "color__name",
            "price",
            "size",
            "type",
        )
        for row in rows:
            row_num += 1
            for col_num, _ in enumerate(row):
                worksheet.write(row_num, col_num, row[col_num], font_style)
        workbook.save(response)
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
            "name",
            "description",
            "category__name",
            "brand__name",
            "color__name",
            "price",
            "size",
            "type",
        )
        for row in rows:
            writer.writerow(row)

        return response


class ProductAjaxDatatableView(AjaxDatatableView):
    model = Product
    title = 'Products'
    initial_order = [["name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'title': 'Product Name', 'name': 'name', 'visible': True, },
        {'title': 'Description', 'name': 'description', 'visible': True, },
        {'title': 'Category', 'name': 'category', 'foreign_field': 'category__name', 'visible': True, },
        {'title': 'Brand', 'name': 'brand', 'foreign_field': 'brand__name', 'visible': True, },
        {'title': 'Color', 'name': 'color', 'foreign_field': 'color__name', 'visible': True, },
        {'title': 'size', 'name': 'price', 'visible': True, },
        {'title': 'Price', 'name': 'size', 'visible': True, },
        {'title': 'Type', 'name': 'type', 'visible': True, },
    ]
