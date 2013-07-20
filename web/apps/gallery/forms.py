from django import forms
from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from web.apps.gallery.models import Image


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100,
                             label='',
                             widget=forms.TextInput(attrs={
                                   'placeholder': 'Voir une galerie',
                                   'class': 'gallery_search',
                                   'type': 'search',
                                   'autocomplete': 'off',
                                   'data-provide': 'typeahead',
                                   'data-source': '[]',
                                   'data-items': '4',
                             }))

    def __init__(self, data_source):
        self.base_fields['search'].widget.attrs['data-source'] = data_source
        super(SearchForm, self).__init__()


class UploadImage(forms.Form):
    img = forms.FileField(
        label='Select an image',
    )
    description = forms.CharField(max_length=200)
    place = forms.CharField(max_length=60)
