from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('', lambda request: redirect('home', permanent=True)),
    path('home', views.home, name='home'),
    path('books', views.book_list, name='book_list'),
    
    # Protecting 'create_book' with login_required so only logged-in users can create books
    path('book/create', login_required(views.create_book), name='book_create'),
    
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    
    # Protecting 'book_update' view with login_required and user_passes_test for Admins or book owner
    path('book/<int:id>/edit/', login_required(user_passes_test(lambda u: u.role == 'ADMIN' or u == u.added_by)(views.book_update)), name='book_update'),
    
    # Protecting 'book_delete' view with user_passes_test for Admins
    path('book/<int:pk>/delete/', login_required(user_passes_test(lambda u: u.role == 'ADMIN')(views.delete_book)), name='book_delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('passwordreset/', views.register, name='passwordreset'),
]

