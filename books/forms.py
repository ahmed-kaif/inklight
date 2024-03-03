from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Review


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]

    # widgets = {
    #     "text": forms.Textarea(
    #         attrs={"rows": 4, "placeholder": "Write your review here..."}
    #     ),
    # }


class BookSearchForm(forms.Form):
    query = forms.CharField(label="Search Books", max_length=100)
