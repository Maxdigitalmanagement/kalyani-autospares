from django import forms
from . models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'enter password',
        'id' : 'password-input',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'confirm password',
        'id' : 'confirm-input',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'enter first name',
        'id' : 'firstname-input',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'enter last name',
        'id' : 'lastname-input',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'enter email',
        'id' : 'email-input',
    }))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder' : 'enter phone number',
        'maxlength' : '10',
        'id' : 'phone-input',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            continue
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )