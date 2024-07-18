from django import forms
from . models import Account, UserAddress, UserProfile

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
        

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'pincode', 'state', 'city']

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['profile_picture']