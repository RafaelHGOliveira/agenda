from django.contrib import admin
from contact import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 
                    'last_name', 'phone', 
                    'email', 'created_date', 
                    'show', )
    list_display_links = ('id', 'first_name', 
                    'last_name', )
    list_filter = ('created_date', )
    search_fields = ('id', 'first_name', 
                    'last_name', 'phone', 
                    'email', )
    ordering = ('id', )
    list_per_page = 10
    list_editable = ('show', )
    
    

# admin.site.register(models.Contact, ContactAdmin)