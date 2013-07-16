from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import *

class Search(Form):
    gallery = CharField(max_length=100)
