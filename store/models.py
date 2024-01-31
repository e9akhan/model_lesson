import random

from django.db import models
from django.db.models import Q, Count
from django.utils.text import slugify
from store.fake import Fake

# Create your models here.

fake = Fake()


class CommonFields(models.Model):
    slug = models.SlugField()
    address = models.TextField()

    class Meta:
        abstract = True


class Profile(CommonFields):
    username = models.CharField(max_length = 20, unique = True)
    email = models.EmailField(primary_key = True)
    phone = models.CharField(max_length = 15)

    class Meta:
        verbose_name = 'Profile Model'

    @classmethod
    def create_random_profiles(cls):
        usernames = fake.create_usernames()
        emails = fake.create_emails()
        phones = fake.create_phone_numbers()
        addresses = fake.create_addresses()

        profile_list = []

        for username, email, phone, address in zip(usernames, emails, phones, addresses):
            profile_list.append(
                cls(
                username = username,
                email = email,
                phone = phone,
                address = address
            )
        )
            
        cls.objects.bulk_create(profile_list)

    @classmethod
    def profile_for_author_name(cls, name):
        name = name.lower()
        user = ''
        
        for profile in cls.objects.all():
            if profile.author.name.lower() == name:
                user = profile
                break

        return user

    def save(self, **kwargs):
        self.slug = slugify(self.username)
        return super().save(**kwargs)

    def __str__(self):
        return self.username


class Author(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    profile = models.OneToOneField(Profile, on_delete = models.CASCADE, related_name = 'author')

    class Meta:
        verbose_name = 'Author Model'

    @classmethod
    def create_random_authors(cls):
        names = fake.create_names()
        profiles = list(Profile.objects.all())

        author_list = []

        for name, profile in zip(names, profiles):
            author_list.append(
                cls(
                name = name,
                profile = profile
            )
        )

        cls.objects.bulk_create(author_list)

    @classmethod
    def all_authors(cls):
        return cls.objects.all()
    
    @classmethod
    def author_with_more_than_2_books(cls):
        return [
            author 
            for author in cls.all_authors()
            if len(author.book_set.all()) > 2
        ]
    
    @classmethod
    def author_with_books_count(cls):
        authors = cls.objects.annotate(count = Count('book'))
        author_books = {}

        for author in authors:
            author_books[author.name] = author_books.get(author.name, 0) + author.count 

        return author_books


    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name


class Publisher(CommonFields):
    name = models.CharField(max_length = 50, unique = True)
    website = models.URLField()
    email = models.EmailField()

    class Meta:
        verbose_name = 'Publisher Model'

    @classmethod
    def create_random_publishers(cls):
        names = fake.create_names()
        websites = fake.create_websites()
        emails = fake.create_emails()
        addresses = fake.create_addresses()

        publisher_list = []

        for name, website, email, address in zip(names, websites, emails, addresses):
            publisher_list.append(
                cls(
                name = name,
                website = website,
                email = email,
                address = address
            )
            )

        cls.objects.bulk_create(publisher_list)

    @classmethod
    def publisher_books_by_name(cls, name):
        books = []
        for publisher in cls.objects.filter(name__icontains = name):
            print(publisher)
            books += list(publisher.book_set.all())

        return books
    
    @classmethod
    def publisher_books_by_website(cls, website):
        books = []
        for publisher in cls.objects.filter(website__icontains = website):
            books += publisher.book_set.all()

        return books

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    genre_choices = [
        ('horror', 'horror'),
        ('self help', 'self help'),
        ('adventure', 'adventure'),
        ('others', 'others')
    ]

    slug = models.SlugField()
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)
    date_of_pub = models.DateField()
    genre = models.CharField(max_length = 20, choices = genre_choices, default = 'others')
    is_deleted = models.BooleanField(default = False)

    class Meta:
        unique_together = ['author', 'title', 'date_of_pub']
        ordering = ['-date_of_pub']
        verbose_name = 'Book Model'

    @classmethod
    def create_random_books(cls):
        authors = list(Author.objects.all())
        titles = fake.create_titles()
        publishers = list(Publisher.objects.all())
        date_of_pubs = fake.create_dates()

        book_list = []

        for title in titles:
            book_list.append(
                cls(
                author = random.choice(authors),
                title = title,
                publisher = random.choice(publishers),
                date_of_pub = random.choice(date_of_pubs)
            )
            )

        cls.objects.bulk_create(book_list)

    @classmethod
    def author_books(cls, name):
        return list(cls.objects.filter(
            author__name = name
        ))

    @classmethod
    def books_with_authors_startswith_a(cls):
        return list(cls.objects.filter(
            author__name__istartswith = 'a'
        ))
    
    @classmethod
    def books_with_authors_endswith_a(cls):
        return list(cls.objects.filter(
            author__name__iendswith = 'a'
        ))
    
    @classmethod
    def books_with_author_and_publisher_name(cls, author_name, publisher_name):
        return list(cls.objects.filter(
            author__name = author_name, publisher__name = publisher_name
        ))
    
    @classmethod
    def books_in_given_year(cls, year):
        return list(
            cls.objects.filter(
            date_of_pub__year = year
        )
        )
    
    @classmethod
    def books_with_publisher_name(cls, name):
        return list(
            cls.objects.filter(
            publisher__name__icontains = name
        )
        )
    
    @classmethod
    def create_book(cls, **kwargs):
        return cls.objects.get_or_create(**kwargs)
    
    @classmethod
    def books_with_publisher_names(cls, names):
        books = []

        for name in names:
            books += cls.books_with_publisher_name(name)

        return books
    
    @classmethod
    def books_with_authors(cls, author1, author2):
        return cls.objects.filter(
            Q(author__name__icontains = author1) &
            Q(author__name__icontains = author2)
        )
    
    @classmethod
    def books_with_exclude_author(cls, name):
        return cls.objects.exclude(
            author__name__icontains = name
        )
    
    @classmethod
    def delete_book(cls, pk):
        try:
            book = cls.objects.get(pk = pk)
            book.delete()
            return "Book successfully deleted."
        except:
            return "Book not found"
        
    @classmethod
    def soft_delete_book(cls, pk):
        try:
            book = cls.objects.get(pk = pk)
            book.is_deleted = True
            book.save()
            return "Book successfully deleted"
        except:
            return "Book not found."

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        return super().save(**kwargs)

    def __str__(self):
        return self.title


class Collection(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    book = models.ManyToManyField(Book)

    class Meta:
        verbose_name = 'Collection Model'
        db_table = 'book_collection'

    @classmethod
    def create_random_collections(cls):
        names = fake.create_names()
        books = list(Book.objects.all())

        for name in names:
            collection = cls.objects.create(
                name = name,
            )

            collection.book.add(random.choice(books))

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)

    def __str__(self):
        return self.name
