from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Book, Review, Author, Category
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ReviewForm,
    BookSearchForm,
)


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("book-list")
    else:
        form = CustomAuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("book-list")


def index(request):
    # books = Book.objects.all()
    # books_json = serializers.serialize("json", books)
    books_json = list(Book.objects.values())
    print(books_json.count)
    return JsonResponse(books_json, safe=False)


def book_list(request):
    books = Book.objects.all()
    context = {
        "books": books,
    }
    return render(request, "book_list.html", context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    reviews = Review.objects.filter(book__id=book.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect("book-details", pk=book.id)
    else:
        form = ReviewForm()
    context = {
        "book": book,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "book_details.html", context)


def search_books(request):
    query = request.GET.get("query", "")
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query)
            | Q(publisher__icontains=query)
            | Q(authors__name__icontains=query)
        ).distinct()

    form = BookSearchForm(initial={"query": query})

    context = {
        "form": form,
        "results": results,
    }

    return render(request, "search_results.html", context)


def author_list(request):
    authors = Author.objects.all()
    context = {
        "authors": authors,
    }
    return render(request, "author_list.html", context)


def category_list(request):
    genres = Category.objects.all()
    context = {
        "genres": genres,
    }
    return render(request, "category_list.html", context)


def dashboard(request):
    return render(request, "profile.html")


# TODO:
# List View
# Details View
# Create View
# Update View
# Delete
