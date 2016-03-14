from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Username or Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class SignupForm(forms.Form):
	email =  forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Email'}))
	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	confirm = forms.CharField(required=True,  widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
	def clean_confirm(self):
		password = self.cleaned_data.get('password')
		confirm = self.cleaned_data.get('confirm')
		if password !=  confirm:
		    raise forms.ValidationError("Confirm Password didnot matched.")
		return confirm

	def clean_username(self):
	    username = self.cleaned_data['username']
	    if User.objects.filter(username=username).exists():
	        raise forms.ValidationError('Username already exists.')
	    return username