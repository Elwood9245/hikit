from django import forms
from .models import Event, Route, UserProfile

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description', 'distance', 'elevation_gain', 'difficulty', 'featured_image']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'max_participants']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'hiking_experience', 'profile_picture', 'phone_number', 'emergency_contact']