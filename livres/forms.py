from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import Book, Review, UserProfile, Book
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

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.AUTH_USER  # Automatically assign role
        if commit:
            user.save()
        return user

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
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Write your thoughts here...'
            }),        
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'favorite_genres', 'badges']
        widgets = {
            'favorite_genres': forms.CheckboxSelectMultiple(choices=Book.GENRE_CHOICES),  # Multi-select checkboxes
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
