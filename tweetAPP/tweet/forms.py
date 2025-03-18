from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TweetForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'What\'s on your mind?'
        }),
        error_messages={
            'required': 'Please enter some content for your tweet.',
            'max_length': 'Your tweet is too long. Please keep it under %(limit_value)d characters.'
        }
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        error_messages={
            'invalid_image': 'The uploaded file is not a valid image.',
            'invalid': 'Please upload a valid image file.'
        }
    )
    
    class Meta:
        model = Tweet
        fields = ['content', 'image']
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content.strip() == '':
            raise forms.ValidationError('Tweet cannot be empty or contain only whitespace.')
        return content

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Please enter your email address.'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
