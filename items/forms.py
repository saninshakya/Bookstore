from django import forms
from category.models import CategoryList
from django.core.validators import URLValidator
from .models import UploadFile, UploadItemBulk, UploadTableofContent, UploadAbstract



class ItemForm(forms.Form):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Book Tilte'}))
	author = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Author'}))
	pub = forms.CharField(label= "Publisher",required=False, widget=forms.TextInput(attrs={'placeholder':'Publication'}))
	pub_date = forms.CharField(label="Publication date", required=False, widget=forms.TextInput(attrs={'placeholder':'Publication Date'}))
	url = forms.URLField(label="URL", required=False, widget=forms.TextInput(attrs={'placeholder':'Author/Publisher URL'}))
	isbn = forms.CharField(label="ISBN", required=False, widget=forms.TextInput(attrs={'placeholder':'ISBN'}))
	lang = forms.CharField(label="Language", required=False, widget=forms.TextInput(attrs={'placeholder':'Edition Language'}))
	awards = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Awards'}))
	summary = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Summary'}))
	category = forms.ChoiceField(required=False)
	local_img = forms.ImageField(label="Local Book Cover Image", required=False)
	table_of_content = forms.FileField(label="Table of Content", required=False)
	abstract = forms.FileField(label="Abstract", required=False)
	img_url = forms.URLField(label="URL of Book Cover Image",required=False, widget=forms.TextInput(attrs={'placeholder':'Book Cover Image URL'}))

	def __init__(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		# For displaying choice list of category
		CHOICES = []
		for category in CategoryList.objects.filter(deleted=False).order_by('category'):
		    CHOICES.append( (category.id, category.category) )
		self.fields['category'].choices = CHOICES

	
class UploadFileForm(forms.ModelForm):

	class Meta:
		model = UploadFile

class UploadTableOfContentForm(forms.ModelForm):

	class Meta:
		model = UploadTableofContent

class UploadAbstractForm(forms.ModelForm):

	class Meta:
		model = UploadAbstract

class SelectXMLForm(forms.ModelForm):
	
	class Meta:
		model = UploadItemBulk

