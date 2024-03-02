from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import Book, Author, Category, Review, Sentiment

# Register your models here.


class BookResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        author_name = row["authors"]
        Author.objects.get_or_create(name=author_name, defaults={"name": author_name})
        category_name = row["categories"]
        Category.objects.get_or_create(
            name=category_name, defaults={"name": category_name}
        )

    categories = fields.Field(
        column_name="categories",
        attribute="categories",
        widget=widgets.ManyToManyWidget(Category, field="name", separator="|"),
    )

    authors = fields.Field(
        column_name="authors",
        attribute="authors",
        widget=widgets.ManyToManyWidget(Author, field="name", separator="|"),
    )

    class Meta:
        model = Book


class BookAdmin(ImportExportModelAdmin):
    resource_classes = [BookResource]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Sentiment)
