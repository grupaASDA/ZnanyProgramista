from django import forms
from django.core.exceptions import ValidationError

from programmers.models import ProgrammerProfile


class ProgrammerCreationModelForm(forms.ModelForm):
    class Meta:
        model = ProgrammerProfile
        fields = ['description', 'experience', 'programming_languages', 'tech_stack', 'wage',
                  'portfolio', 'phone']

    def clean_wage(self):
        wage = self.cleaned_data["wage"]
        if wage <= 0:
            raise ValidationError("Wage must be bigger than zero")
        return wage

    def save(self, commit=True):
        programmer = super(ProgrammerCreationModelForm, self).save(commit=False)
        if commit:
            programmer.save()
        if self.cleaned_data['programming_languages']:
            programmer.programming_languages = self.cleaned_data['programming_languages']
        return programmer


class RatingForm(forms.Form):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)


class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField()
