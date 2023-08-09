from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation, authenticate
from django.shortcuts import render, redirect
from .models import Customer, DesignerPlaced



class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}




class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))





class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus':True, 'class': 'form-control'}), help_text= password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocompplete': 'new-password', 'class': 'form-control'})
    )


from django.core.exceptions import ValidationError
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'locality', 'city', 'state', 'zipcode', ]
        widgets = {'name':forms.TextInput(attrs={'class':'form_control'}), 'phone':forms.NumberInput(attrs={'class':'form-control'}), 'locality':forms.TextInput(attrs={'class':'form_control'}),
                'city':forms.TextInput(attrs={'class':'form_control'}), 'state':forms.Select(attrs={'class':'form_control'}), 'zipcode':forms.NumberInput(attrs={'class':'form-control'})}

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Remove any non-digit characters from the phone number
        phone = ''.join(filter(str.isdigit, str(phone)))

        if len(phone) != 10 :
            raise ValidationError(_('Invalid phone number. Please enter a 10-digit Indian phone number.'))

        return phone  


from django import forms
from .models import DESIGNER_STATUS_CHOICES

class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=DESIGNER_STATUS_CHOICES)




from django import forms
from .models import DesignerWorks

class DesignerWorksForm(forms.ModelForm):
    class Meta:
        model = DesignerWorks
        fields = ['works_img', 'descriptions']




# forms.py
# app/forms.py

from django import forms
from .models import Designer

class DesignerProfileForm(forms.ModelForm):
    class Meta:
        model = Designer
        fields = ['full_name', 'email', 'phone', 'work_exp', 'address', 'zipcode', 'state', 'designer_image']

