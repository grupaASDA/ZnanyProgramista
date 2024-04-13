from django import forms

from communication.models import Communicate

class CommunicationCreationModelForm(forms.ModelForm):
    class Meta:
        model = Communicate
        fields = ['title', 'contents']
