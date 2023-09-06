from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact
from django.http import Http404
from django.contrib.auth.decorators import login_required


@login_required(login_url='contact:login')
def index(request):
    contacts = Contact.objects \
        .filter(show=True)\
            .filter(owner=request.user,)\
                .order_by('-id')
            
    paginator = Paginator(contacts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - ',
    }
    
    return render(
        request,
        'contact/index.html',
        context,
    )

@login_required(login_url='contact:login')
def search(request):
    search_value = request.GET.get('q', '').strip()
    
    # Checking if is a empty value on search
    if search_value == '':
        return redirect('contact:index')
    
    contacts = Contact.objects \
        .filter(show=True) \
            .filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(phone__icontains=search_value) |
                Q(email__icontains=search_value)
            ) \
                .filter(owner=request.user,)\
                    .order_by('-id')
            
    paginator = Paginator(contacts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Search - ',
    }
    
    return render(
        request,
        'contact/index.html',
        context,
    )
    
@login_required(login_url='contact:login')
def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(
        Contact, 
        pk=contact_id,
        show=True,
        owner=request.user,
    )

    site_title = f'{single_contact.first_name} {single_contact.last_name} - '
    
    context = {
        'contact': single_contact,
        'site_title': site_title,
    }
    
    return render(
        request,
        'contact/contact.html',
        context,
    )
