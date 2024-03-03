from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("books/", views.book_list, name="book-list"),
    path("books/<int:pk>", views.book_details, name="book-details"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
