from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    
    # face_image = forms.ImageField(required=True)
    # changed to false because it is dynamically filled 
    face_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "face_image",
            "password1",
            "password2",
        ]


# profiles/forms.py


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
