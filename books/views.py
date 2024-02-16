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


# TODO:
# List View
# Details View
# Create View
# Update View
# Delete
