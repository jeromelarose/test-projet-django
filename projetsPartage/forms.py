from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users
from rest_framework_simplejwt.tokens import RefreshToken  # Ajoute cet import

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'password', 'mail', 'picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Optionnel : Ajoute une validation personnalisée si nécessaire
        if not Users.objects.filter(username=username).exists():
            raise forms.ValidationError("Nom d'utilisateur non valide.")
        return cleaned_data