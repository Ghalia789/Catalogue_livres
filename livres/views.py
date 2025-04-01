from django.shortcuts import get_object_or_404, redirect, render
from .models import Book
from .forms import BookForm


# Create your views here.
def home(request):
    return render(request, 'livres/index.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'livres/book_list.html', {'books': books})


def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)  # Add request.FILES for images
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list page
    else:
        form = BookForm()
    
    return render(request, 'livres/create_book.html', {'form': form})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'livres/book_detail.html', {'book': book})

def book_update(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk )
    else:
        form = BookForm(instance=book)

    return render(request, 'livres/book_update.html', {'form': form, 'book': book})