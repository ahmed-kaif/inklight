from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


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
    all_books_list = Book.objects.order_by("title")
    books_per_page = 36

    # Paginate the books
    paginator = Paginator(all_books_list, books_per_page)
    page = request.GET.get("page", 1)
    books = paginator.get_page(page)
    context = {
        "books": books,
    }
    return render(request, "book_list.html", context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    reviews = Review.objects.filter(book__id=book.id)
    user_reviews = Review.objects.filter(user=request.user.id, book=book)

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

    #  if user has review then dont pass the form
    context = {
        "book": book,
        "reviews": reviews,
        "stars": [1, 2, 3, 4, 5],
    }
    if not user_reviews.exists():
        context["form"] = form
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
    authors = Author.objects.order_by("name")
    context = {
        "authors": authors,
    }
    return render(request, "author_list.html", context)


def category_list(request):
    categories = Category.objects.order_by("name")
    context = {
        "categories": categories,
    }
    return render(request, "category_list.html", context)


def books_by_author(request, author_name):
    # Retrieve books based on author name
    books = Book.objects.filter(authors__name__icontains=author_name)

    context = {
        "author_name": author_name,
        "books": books,
    }

    return render(request, "books/books_by_author.html", context)


def books_by_category(request, category_name):
    # Retrieve books based on genre name
    books = Book.objects.filter(categorys__name__icontains=category_name)

    context = {
        "category_name": category_name,
        "books": books,
    }

    return render(request, "books/books_by_category.html", context)


@login_required
def profile(request):
    user_reviews = Review.objects.filter(user=request.user)
    reviewed_books = Book.objects.filter(
        id__in=user_reviews.values_list("book_id", flat=True)
    )
    context = {
        "books": reviewed_books,
    }

    return render(request, "profile.html", context)


# TODO:
# List View
# Details View
# Create View
# Update View
# Delete
