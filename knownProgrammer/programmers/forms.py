from django import forms
from django.core.exceptions import ValidationError

from programmers.models import ProgrammerProfile


class ProgrammerCreationModelForm(forms.ModelForm):
    class Meta:
        model = ProgrammerProfile
        fields = ['description', 'experience', 'programming_languages', 'tech_stack', 'wage_min', 'wage_max',
                  'portfolio', 'phone']

    def clean_wage_min(self):
        wage_min = self.cleaned_data["wage_min"]
        if wage_min <= 0:
            raise ValidationError("Wage_min must be bigger than zero")
        return wage_min

    def clean_wage_max(self):
        wage_max = self.cleaned_data["wage_max"]
        wage_min = self.cleaned_data["wage_min"]
        if wage_max <= 0:
            raise ValidationError("Wage max must be bigger than zero")
        if wage_min > wage_max:
            raise ValidationError("Wage max must be bigger than or equal to wage min")
        return wage_max

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
