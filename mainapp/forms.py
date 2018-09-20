from django import forms

from mainapp.models import UploadFile


class UploadFileForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()

    class Meta:
        model = UploadFile
        fields = '__all__'