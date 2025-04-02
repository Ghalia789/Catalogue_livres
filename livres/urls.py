from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('home', permanent=True)),
    path('home', views.home, name='home'),  # Home page
    path('books', views.book_list, name='book_list'),
    path('book/create', views.create_book, name='book_create'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:id>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.delete_book, name='book_delete'),
]
