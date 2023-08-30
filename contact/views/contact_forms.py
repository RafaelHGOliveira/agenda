from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404

from contact.models import Contact
from contact.forms import ContactForm


def create(request):
    
    if request.method == 'POST':
        context = {
            'form': ContactForm(data=request.POST),
        }
    
    if request.method == 'GET':
        context = {
            'form': ContactForm(),
        }
    
    
    return render(
        request,
        'contact/create.html',
        context,
    )
    