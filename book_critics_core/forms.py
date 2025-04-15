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
    username = forms.CharField(max_length=50, label='User name')
    email = forms.EmailField(max_length=100, label='email')
    password = forms.CharField(widget=forms.PasswordInput, label='Passsword')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirme your password')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username is already taken")

        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already taken")
        return email


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError("Password must be at least 5 characters long")
        return password


    def clean_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')        

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return confirm_password
    

# Creating Ticket Form ModelForm
class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Ticket.objects.filter(title=title).exists():
            raise forms.ValidationError("The title already exists")

        return title



# Creating Review Form
RATING_CHOICES = [(i, str(i)) for i in range(1,6)] 

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=RATING_CHOICES)
        }


    def clean_headline(self):
        headline = self.cleaned_data.get('headline')
        if Review.objects.filter(headline=headline).exists():
            raise forms.ValidationError("The headline already exists")

        return headline
