from django import forms

from .models import Exhibit, ReflectionExhibit, Route


class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = ("name", "description", "address")


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("title", "description", "route_map")


class ReviewOnExhibitForm(forms.ModelForm):
    class Meta:
        model = ReflectionExhibit
        fields = ("author", "text", "exhibit")
