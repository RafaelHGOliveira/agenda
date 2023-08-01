from django.contrib import admin
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 
                    'last_name', 'phone', 
                    'email', 'created_date', )
    
    

admin.site.register(Contact, ContactAdmin)