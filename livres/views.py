from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from .models import Book, User, Review
from .forms import BookForm, ReviewForm, UserRegisterForm, UserLoginForm

# Helper functions for permissions
def is_admin(user):
    return user.is_authenticated and user.role == User.Role.ADMIN

def is_authenticated_user(user):
    return user.is_authenticated and user.role == User.Role.AUTH_USER

# Auth Views
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'livres/index.html')

def book_list(request):
    books = Book.objects.all()
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')
    genre_query = request.GET.get('genre', '')
    rating_filter = request.GET.get('rating', '')
    published_date = request.GET.get('date', '')

    # Apply search and filters
    if title_query:
        books = books.filter(title__icontains=title_query)

    if author_query:
        books = books.filter(author__icontains=author_query)

    if genre_query:
        books = books.filter(genre__icontains=genre_query)

    if rating_filter:
        if rating_filter == '4+':
            books = books.filter(average_rating__gte=4)
        elif rating_filter == '5':
            books = books.filter(average_rating=5)

    if published_date:
        books = books.filter(published_date=published_date)

    genres = [genre[0] for genre in Book.GENRE_CHOICES]
    context = {
        'books': books,
        'title_query': title_query,
        'author_query': author_query,
        "genres": genres,
        'genre_query': genre_query,
        'rating_filter': rating_filter,
        'published_date': published_date,
    }
    return render(request, 'livres/book_list.html', context)

# Admin Only: Create Book
@user_passes_test(is_admin, login_url='/login/')
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            #book.added_by = request.user  # Track who added the book
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'livres/create_book.html', {'form': form})

# View Book Detail (Editable by owner or admin)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    can_edit = request.user == book.added_by or is_admin(request.user)
    return render(request, 'livres/book_detail.html', {
        'book': book,
        'can_edit': can_edit
    })

# Update Book (Only by admin or the user who added it)
@login_required
def book_update(request, id):
    book = get_object_or_404(Book, id=id)
    
    # Permission check
    if not (request.user == book.added_by or is_admin(request.user)):
        raise PermissionDenied
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'livres/book_update.html', {'form': form, 'book': book})

# Admin Only: Delete Book
@user_passes_test(is_admin, login_url='/login/')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
    return redirect(reverse('book_list'))
#--------------Review--------------
@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            try:
                review.save()
                book.update_average_rating()
                return redirect('book_detail', pk=book.pk)
            except IntegrityError:
                form.add_error(None, "You have already reviewed this book.")
        else:
            print(form.errors)
    else:
        form = ReviewForm()

    return render(request, 'livres/add_review.html', {'form': form, 'book': book})
#@user_passes_test(is_admin, login_url='/login/')
#def delete_review(request, review_id):
     # Review form handling here
     
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure the logged-in user is the owner of the review
    if review.user != request.user:
        return redirect('book_detail', pk=review.book.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=review.book.id)

    else:
        form = ReviewForm(instance=review)

    return render(request, 'livres/update_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Allow deletion if user is owner or admin
    if review.user == request.user or request.user.is_superuser or getattr(request.user, 'role', None) == 'ADMIN':
        review.delete()

    return redirect('book_detail', book_id=review.book.id)