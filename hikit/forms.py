from django import forms
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'description', 'distance', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
