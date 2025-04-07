from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.apps import apps

User = get_user_model()
Ticket = apps.get_model('book_critics_core', 'Ticket')
Review = apps.get_model('book_critics_core', 'Review')


# Creating Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Nom d\'utilisateur')
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
    username = forms.CharField(max_length=50, label='Nom d\'utilisateur')
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


# Creating Ticket Form
class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, label='Title')
    description = forms.CharField(widget=forms.Textarea, max_length='350', label='Description')
    image = forms.ImageField(label='Image', required=False)
    username = forms.CharField(max_length=50,
                               widget=forms.HiddenInput(),
                                label='User\'s name'
                                )


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        username = cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username does not exist")

        if Ticket.objects.filter(title=title).exists():
            raise forms.ValidationError("The title already exists")

        return cleaned_data


# Creating Review Form
class ReviewForm(forms.Form):
    headline = forms.CharField(max_length=128, label='Title')
    body = forms.CharField(widget=forms.Textarea, max_length=500, label='Body')
    rating = forms.IntegerField(min_value=0, max_value=5, label='Rating')
    username = forms.CharField(max_length=50,
                               widget=forms.HiddenInput(),
                                label='User\'s name'
                                )

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get('headline')
        username = cleaned_data.get('username')

        print("ALL: ", headline, username)

        if Review.objects.filter(headline=headline).exists():
            print("HEADLINE: ", headline)
            raise forms.ValidationError("The headline already exists")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username does not exist")

        return cleaned_data
