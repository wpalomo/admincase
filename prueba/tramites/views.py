from django.shortcuts import render
from django.views.generic import CreateView
from .models import RequisitosPresentados
from .forms import RequisitoForm
# Create your views here.

class RequisitoCreate(CreateView):
    model = RequisitosPresentados
    form_class = RequisitoForm