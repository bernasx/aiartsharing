from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import EmailField
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    # Django probably requires the LoginView to be tied into the "username" name for authentication,
    # so we have to work around that and make this an email field, and make the template properly
    # handle the special username case
    username = EmailField(label='Email', required=True)
        
