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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Changing plaholder 
        # without recreating TextInput widget
        # self.fields['first_name'].widget.attrs.update({
        #     'placeholder': 'first name',
        # })
    
    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            # 'picture',
        )
        
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'first name',
        #         }
        #         ),
        # }
    
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

        # self.add_error(
        #     'first_name',
        #     ValidationError(
        #         'Erro',
        #         code='invalid',
        #     )
        # )
        
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