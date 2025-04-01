from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # HTML5 date picker
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'genre', 'published_date', 'isbn', 'cover_image']
