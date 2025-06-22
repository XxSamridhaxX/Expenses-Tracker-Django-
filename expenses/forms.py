from django import forms
from .models import Expense,User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class ExpenseForm(forms.ModelForm):
    class Meta:
        model= Expense
        fields=['title','amount','category','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        # It customizes the HTML widget used for the date field in your form by using an HTML <input type="date">.
        # Yo mathi ko add garena bhane date manually lekhnu parcha like 2/5/2025 bhanera tra hamle use garem bhane chai hamle select garna milcha date



class EmailLoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    # password=forms.CharField(widget=forms.PasswordInput)
    # Creates Input field for Email and Password in form <input type="password" name="password">


    def clean(self):
        # This method is called when you use user.is_valid()
        email= self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        # cleaned_data is a dictionary of data which is validated it contains data in the form of key and value

        try:
            user= User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with this email")
        
        user=authenticate(username=user.username,password=password)
        
        if user is None:
            raise forms.ValidationError("Incorrect password")
        
        self.user=user
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model= User
        fields=['username','email','password1','password2']
