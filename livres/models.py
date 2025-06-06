from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

#User model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        AUTH_USER = 'AUTH_USER', 'Authenticated User'
        VISITOR = 'VISITOR', 'Visitor'
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.AUTH_USER)
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
    
    def get_average_rating(self):
        reviews = self.reviews.all()  # Assuming a reverse relationship from Review to Book
        total_rating = sum([review.rating for review in reviews])
        count = len(reviews)
        if count > 0:
            return total_rating / count
        return 0  # Return 0 if there are no reviews yet
    def update_average_rating(self):
        self.average_rating = self.get_average_rating()
        self.save(update_fields=['average_rating'])
        
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')  # Optional: prevent duplicate reviews by same user
class UserGenre(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Mystery', 'Mystery'),
        ('Fantasy', 'Fantasy'),
        ('Biography', 'Biography'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('Horror', 'Horror'),
        ('Young Adult', 'Young Adult'),
        # Add more if you want
    ]

    name = models.CharField(max_length=100, choices=GENRE_CHOICES, unique=True)

    def __str__(self):
        return self.name
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    favorite_genres = models.ManyToManyField(UserGenre, blank=True)
    badges = models.JSONField(default=list)

    def __str__(self):
        return self.user.username

    def average_rating(self):
        return self.user.review_set.aggregate(models.Avg('rating'))['rating__avg']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)
        instance.userprofile.save()


