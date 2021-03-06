from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
                        required=True, 
                        widget=forms.TextInput(
                                attrs={
                                    "placeholder": "+2348132450841 or 08132450841",
                                }
                            )
                        )
    pick_up_address = forms.CharField(
                        required=True,
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Our courier picks up the gadget from this address",
                                }
                            )
                        )
    state = forms.CharField(
                        required=True, 
                        widget=forms.TextInput(
                                attrs={
                                    "placeholder": "e.g LAGOS",
                                }
                            )
                        )
    
    city = forms.CharField(
                        required=True, 
                        widget=forms.TextInput(
                                attrs={
                                    "placeholder": "e.g LAGOS",
                                }
                            )
                        )
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'pick_up_address', 'state', 'city']
