from django.contrib import admin
from store.models import Profile, Book, Author, Publisher, Collection

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['slug', 'username', 'email', 'phone', 'address']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['slug', 'author', 'title', 'publisher', 'date_of_pub', 'is_deleted']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'profile']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'website', 'email', 'address']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name']