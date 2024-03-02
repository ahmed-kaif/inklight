from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import Book

# Create your views here.


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
    context = {
        "book": book,
    }
    return render(request, "book_details.html", context)


def dashboard(request):
    return render(request, "profile.html")


# TODO:
# List View
# Details View
# Create View
# Update View
# Delete
