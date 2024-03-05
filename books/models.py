from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from textblob import TextBlob
from django.template.defaultfilters import slugify


# Create your models here.

# TODO:
# Categories
# Authors
# Books
# Reviews
# User


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    image = models.URLField(null=True, blank=True)
    publisher = models.CharField(max_length=100)
    published_at = models.CharField(max_length=20, null=True, blank=True)
    no_of_pages = models.PositiveSmallIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    total_review = models.PositiveIntegerField(null=True, blank=True)
    imported = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book-details", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Sentiment(models.Model):
    title = models.CharField(max_length=200)
    value = models.SmallIntegerField()

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    sentiment = models.ForeignKey(
        Sentiment, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Perform sentiment analysis after saving the review
        super().save(*args, **kwargs)

        if not self.sentiment and self.text:
            # Use TextBlob for sentiment analysis
            analysis = TextBlob(self.text)

            # Map polarity scores to sentiment labels
            sentiment_mapping = {
                "very negative": -1.0,
                "negative": -0.5,
                "neutral": 0.0,
                "positive": 0.5,
                "very positive": 1.0,
            }

            # Get the sentiment label based on the polarity score
            sentiment_score = analysis.sentiment.polarity
            sentiment_label = max(
                sentiment_mapping,
                key=lambda k: (
                    sentiment_mapping[k]
                    if sentiment_mapping[k] <= sentiment_score
                    else float("-inf")
                ),
            )

            # Create or retrieve the Sentiment model instance
            sentiment, created = Sentiment.objects.get_or_create(
                title=sentiment_label, value=sentiment_mapping[sentiment_label]
            )

            # Assign the sentiment to the review
            self.sentiment = sentiment

            # Save the review again with the sentiment
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.sentiment}"
