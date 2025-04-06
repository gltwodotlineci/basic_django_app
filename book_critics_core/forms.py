from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

# Creating Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        error_message = "Invalid username or password"

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(error_message)

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(error_message)

        return cleaned_data


# Creating Signup Form
class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nom d\'utilisateur')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username is already taken")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
