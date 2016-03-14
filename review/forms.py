from django import forms


class ReviewForm(forms.Form):
	review = forms.CharField(label="",
	required=True, 
	widget=forms.Textarea(attrs={'placeholder':'Write Your Review'}
	))

