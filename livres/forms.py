from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import Book
#BookForm
class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'genre', 
                'published_date', 'isbn', 'cover_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and not self.user.role == 'ADMIN':
            self.fields['cover_image'].disabled = True  # Example restriction

User = get_user_model()  # Gets your custom User model
#Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.VISITOR,
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
#Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')  # Allow email login
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

#Password Reset Form
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )