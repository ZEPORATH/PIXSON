from django.forms import forms
from django.forms import ModelForm
from .models import Opencv, Opencv2


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class FormOpencv(ModelForm):
    class Meta:
        model = Opencv
        fields = ['imagem']


class ResizerInputs(ModelForm):
    class Meta:
        model = Opencv2
        fields = ['height','width','resize_method']


