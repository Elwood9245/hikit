from django import forms
from .models import Event, Route, UserProfile
from django.core.exceptions import ValidationError

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description', 'distance', 'elevation_gain', 'difficulty', 'featured_image']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'max_participants', 'status']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'max_participants': 'Maximum Participants',
            'status': 'Event Status'
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Share something about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'profile_picture': "Profile Photo"
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['bio'].initial = self.user.profile.bio if hasattr(self.user, 'profile') else ''

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2*1024*1024:  # 2MB limit
                raise ValidationError("Image too large (max 2MB)")
            if not picture.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Only JPG/PNG images allowed")
        return picture

