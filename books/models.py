from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

# TODO:
# Categories
# Authors
# Books
# Reviews
# User

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    authors = models.ManyToManyField(Author, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    image = models.CharField(max_length=300, blank=True)
    publisher = models.CharField(max_length=100)
    published_at = models.CharField(max_length=20, null=True, blank=True)
    imported = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.book.title}"
