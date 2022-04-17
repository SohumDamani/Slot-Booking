from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        if CustomUser.objects.filter(username=cleaned_data["username"]).exists():
            raise forms.ValidationError("The username is taken, please try another one")
