from django import forms

from .models import Exhibit


class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        exclude = ('order',)
