from django.shortcuts import render

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
    