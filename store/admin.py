"""
    Module name :- admin
"""

from django.contrib import admin
from store.models import Profile, Book, Author, Publisher, Collection


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile admin class.
    """

    list_display = ["slug", "username", "email", "phone", "address"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Book admin class.
    """

    list_display = ["slug", "author", "title", "publisher", "date_of_pub", "is_deleted"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Author admin class.
    """

    list_display = ["slug", "name", "profile"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Publisher admin class.
    """

    list_display = ["slug", "name", "website", "email", "address"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    Collection admin class.
    """

    list_display = ["slug", "name"]
