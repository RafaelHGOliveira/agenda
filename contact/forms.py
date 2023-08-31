from contact.models import Contact
from django import forms
from django.forms import ValidationError


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'first name',
                }
            ),
        label = 'First Name',
        # help_text = 'teste help test',
        )
    
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )
    
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
        )
        
    
    # Better to verify multiple fields
    def clean(self):
        
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        
        if first_name == last_name:
            msg = ValidationError(
                    'First and Last Name cannot be the same',
                    code='invalid',
                )
            
            self.add_error(
                'first_name',
                msg,
            )
            self.add_error(
                'last_name',
                msg,
            )
        
        return super().clean()
    
    
    # Verify error on a single field
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'ABC':
            raise ValidationError(
                'Erro',
                code='invalid',
            )
        
        return first_name