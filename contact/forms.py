from contact.models import Contact
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation



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
                'accept': 'image/*'
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


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    # Editing firlds used on default user creation form
    class Meta():
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )
    
    
    # Check if email is already been used
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'The email is already being used',
                    code='invalid'
                )
            )
        
        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    
    password1 = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    
    class Meta():
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )
        
    # Overriding save function to save password
    # in case of change
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        
        password1 = cleaned_data.get('password1')
        
        if password1:
            user.set_password(password1)
        
        if commit:
            user.save()
            
        return user
        
    # overriding clean to check if passwords match
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError(
                        'Passwords dont match',
                    )
                )

        return super().clean()
        
    
    # Check if email is already been used
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        
        # Checking if its not te same as the old email
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'The email is already being used',
                        code='invalid',
                    )
                )
        
        return email
    
    # Checking if its a strong password
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
           try:
               password_validation.validate_password(password1)
           except ValidationError as errors:
               self.add_error(
                   'password1',
                   ValidationError(
                       errors,
                    ),
               )
            
            
        return password1