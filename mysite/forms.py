
from django.forms import ModelForm

from modelView.models import Account
from modelView.models import Media

class accountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

class mediaForm(ModelForm):
    class Meta:
        model = Media

# class UploadFileForm(forms.Form):
#    	title=forms.CharField(max_length=50)
#    	file=forms.FileField()