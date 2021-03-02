""" product forms"""
import re

from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    """ This class will handle the form and validate it."""

    file = forms.FileField(
        label="File",
        required=False,
        validators=[
            FileExtensionValidator(allowed_extensions=["xlsx", "csv"])
        ],
    )
    url = forms.URLField(label="Url of G-sheet", required=False)

    def clean(self):
        """
        custom validate url of google sheet
        validation for either url or file should be in post data
        """
        super().clean()
        url = self.cleaned_data.get("url")
        file = self.cleaned_data.get("file")
        if url:
            regex = re.search(
                r"https://docs.google.com/spreadsheets/d/([-\w]+)/", url
            )
            if not regex:
                raise forms.ValidationError("Invalid Google Sheet link")
        if not url and not file:
            raise forms.ValidationError("Upload File or Enter URL")
        return self.cleaned_data
