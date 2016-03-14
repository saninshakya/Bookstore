from django import forms

class CategoryForm(forms.Form):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Category Ttile'}))