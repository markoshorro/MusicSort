from django import forms
 
from models import UploadFile
 
 
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        # This param is needed now
        fields = ['file']
