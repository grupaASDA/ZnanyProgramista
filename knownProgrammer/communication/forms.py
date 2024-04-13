from django import forms

from communication.models import Message

class MessageCreationModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']
