from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    path("profile/", views.profile, name="profile"),
    path("books/", views.book_list, name="book-list"),
    path("books/<int:pk>", views.book_details, name="book-details"),
    path("books/search/", views.search_books, name="search_books"),
    path(
        "books/author/<str:name>/",
        views.books_by_author,
        name="books_by_author",
    ),
    path(
        "books/genre/<str:category_name>/",
        views.books_by_category,
        name="books_by_category",
    ),
    path("authors/", views.author_list, name="author-list"),
    path("genres/", views.category_list, name="category-list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
