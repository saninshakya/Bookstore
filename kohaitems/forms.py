from django import forms


class IsbnForm(forms.Form):
	isbn = forms.CharField(label="ISBN", required=False, widget=forms.TextInput(attrs={'placeholder':'ISBN'}))