from django.db import models
from django.contrib.auth.models import AbstractUser

#User model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        AUTH_USER = 'AUTH_USER', 'Authenticated User'
        VISITOR = 'VISITOR', 'Visitor'
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VISITOR)
    #properties for easier permission checking
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_authenticated_user(self):
        return self.role == self.Role.AUTH_USER
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
#Book model
class Book(models.Model):
    # Genre constants
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCI_FI = 'Sci-Fi'
    MYSTERY = 'Mystery'
    FANTASY = 'Fantasy'
    BIOGRAPHY = 'Biography'
    HISTORICAL_FICTION = 'Historical Fiction'
    THRILLER = 'Thriller'
    ROMANCE = 'Romance'
    HORROR = 'Horror'
    ADVENTURE = 'Adventure'
    YOUNG_ADULT = 'Young Adult'
    CHILDRENS = "Children's Fiction"
    POETRY = 'Poetry'
    SELF_HELP = 'Self-Help'
    PHILOSOPHY = 'Philosophy'
    TRUE_CRIME = 'True Crime'
    SCIENCE = 'Science'
    HEALTH_WELLNESS = 'Health & Wellness'
    ART_PHOTOGRAPHY = 'Art & Photography'
    BUSINESS_ECONOMICS = 'Business & Economics'
    COOKING_FOOD = 'Cooking/Food'
    TRAVEL = 'Travel'
    RELIGION_SPIRITUALITY = 'Religion & Spirituality'
    POLITICS = 'Politics'
    PSYCHOLOGY = 'Psychology'
    DRAMA = 'Drama'
    GRAPHIC_NOVELS = 'Graphic Novels/Comics'
    WESTERN = 'Western'

    # Genre choices using constants
    GENRE_CHOICES = [
        (FICTION, 'Fiction'),
        (NON_FICTION, 'Non-Fiction'),
        (SCI_FI, 'Sci-Fi'),
        (MYSTERY, 'Mystery'),
        (FANTASY, 'Fantasy'),
        (BIOGRAPHY, 'Biography'),
        (HISTORICAL_FICTION, 'Historical Fiction'),
        (THRILLER, 'Thriller'),
        (ROMANCE, 'Romance'),
        (HORROR, 'Horror'),
        (ADVENTURE, 'Adventure'),
        (YOUNG_ADULT, 'Young Adult'),
        (CHILDRENS, "Children's Fiction"),
        (POETRY, 'Poetry'),
        (SELF_HELP, 'Self-Help'),
        (PHILOSOPHY, 'Philosophy'),
        (TRUE_CRIME, 'True Crime'),
        (SCIENCE, 'Science'),
        (HEALTH_WELLNESS, 'Health & Wellness'),
        (ART_PHOTOGRAPHY, 'Art & Photography'),
        (BUSINESS_ECONOMICS, 'Business & Economics'),
        (COOKING_FOOD, 'Cooking/Food'),
        (TRAVEL, 'Travel'),
        (RELIGION_SPIRITUALITY, 'Religion & Spirituality'),
        (POLITICS, 'Politics'),
        (PSYCHOLOGY, 'Psychology'),
        (DRAMA, 'Drama'),
        (GRAPHIC_NOVELS, 'Graphic Novels/Comics'),
        (WESTERN, 'Western'),
    ]

    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)  # Optional, but useful for tracking
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    average_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    #Book Ownership Tracking
    added_by = models.ForeignKey(
        User,  # References your custom User model
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title
    
    #def get_average_rating(self):
    #    reviews = self.reviews.all()  # Assuming a reverse relationship from Review to Book
    #    total_rating = sum([review.rating for review in reviews])
    #    count = len(reviews)
    #    if count > 0:
    #        return total_rating / count
    #    return 0  # Return 0 if there are no reviews yet

