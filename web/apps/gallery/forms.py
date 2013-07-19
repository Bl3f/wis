from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import *

from .models import Image

class Search(Form):
    gallery = CharField(max_length=100)


class DocumentForm(Form):
    docfile = FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class UploadFileForm(Form):
    title = CharField(max_length=50)
    description = CharField(max_length=200)
    file  = FileField()
    
class UploadImage(Form):
    img = FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

def handle_upload(img):
    with open('upload/img.jpg', 'wb+') as destination:
        for chunk in img.chunks():
            destination.write(chunk)
