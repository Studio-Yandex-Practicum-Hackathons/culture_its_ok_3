from django import forms

from .models import Exhibit, Route, ReviewOnExhibit, ReviewOnRoute


class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = ("name", "image", "description", "address")


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("title", "description", "route_map")


class ReviewOnExhibitForm(forms.ModelForm):
    class Meta:
        model = ReviewOnExhibit
        fields = ("author", "text", "exhibit")


class ReviewOnRouteForm(forms.ModelForm):
    class Meta:
        model = ReviewOnRoute
        fields = ("author", "text", "route")

#-------------
from .models import Profile
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }
