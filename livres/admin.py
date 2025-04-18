from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, User

# Book Admin (keep your existing configuration)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_date', 'average_rating', 'created_at', 'added_by')
    list_filter = ('genre', 'published_date', 'added_by')
    search_fields = ('title', 'author')
    raw_id_fields = ('added_by',)  # Better for large user databases

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(added_by=request.user)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

# Register your models
admin.site.register(Book, BookAdmin)
admin.site.register(User, CustomUserAdmin)