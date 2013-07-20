from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import *

from .models import Image


class Search(Form):
    gallery = CharField(max_length=100)


class UploadImage(Form):
    img = FileField(
        label='Select an image',
    )
    description = CharField(max_length=200)
    place = CharField(max_length=60)
