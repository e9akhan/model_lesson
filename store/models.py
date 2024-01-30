import random
from django.utils.text import slugify
from datetime import date, timedelta

from django.db import models


alphabets = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z'
]

numbers = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0'
]


# Create your models here.
class CommonFields(models.Model):
    slug = models.SlugField()
    address = models.TextField()

    class Meta:
        abstract = True

    @staticmethod
    def create_emails():
        email_name = "".join(random.choices(alphabets, k=8))
        return email_name + '@gmail.com'

    @staticmethod
    def create_address():
        return "".join(random.choices(alphabets, k=10)) + ' ' + "".join(random.choices(alphabets, k=10))


class Profile(CommonFields):
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length = 15)
    email = models.EmailField()

    @staticmethod
    def create_username():
        return f'''{"".join(random.choices(alphabets, k=6))}@{random.choice(numbers)[0]}{random.choice(numbers)[0]}{random.choice(numbers)[0]}'''
    
    @staticmethod
    def create_phone_numbers():
        return "".join(random.choices(numbers, k=10))
    
    @classmethod
    def create_random_profiles(cls):
        for _ in range(50000):
            cls.objects.create(
                username = cls.create_username(),
                phone = cls.create_phone_numbers(),
                email = cls.create_emails(),
                address = cls.create_address()
            )

    def save(self, **kwargs):
        self.slug = slugify(self.username + self.email)
        return super().save(**kwargs)

    def __str__(self):
        return self.username


class Author(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name = 'author')

    @classmethod
    def all_authors(cls):
        return list(cls.objects.all())
    
    @property
    def author_books(self):
        return self.book_set.all()
    
    @classmethod
    def author_with_more_than_2_books(cls):
        return [author for author in cls.objects.all() if len(author.author_books) > 2]
    
    def get_user_details(self):
        return self.name, self.profile
    
    @staticmethod
    def create_name():
        return "".join(random.choices(alphabets, k=8))

    @classmethod
    def create_authors(cls):
        profiles = list(Profile.objects.all())

        for i in range(50000):
            cls.objects.create(
                name = cls.create_name(),
                profile = profiles[i]
            )
    
    def save(self, **kwargs):
        self.slug = slugify(self.name + self.profile.username)
        return super().save(**kwargs)
    
    def __str__(self):
        return self.name


class Publisher(CommonFields):
    name = models.CharField(max_length = 50)
    website = models.URLField()
    email = models.EmailField()

    def published_books(self):
        return self.book_set.all()

    @staticmethod
    def create_name():
        return "".join(random.choices(alphabets, k=8))
    
    @staticmethod
    def create_website():
        return f'{"".join(random.choices(alphabets, k=8))}.com'

    @classmethod
    def create_random_publishers(cls):
        for _ in range(50000):
            cls.objects.create(
            name = cls.create_name(),
            email = cls.create_emails(),
            website = cls.create_website(),
            address = cls.create_address()
        )

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    slug = models.SlugField()
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)
    date_of_pub = models.DateField()

    @classmethod
    def books_with_author_name_starts_with_a(cls):
        return cls.objects.filter(author__name__istartswith = 'a')

    @classmethod
    def books_with_author_name_ends_with_a(cls):
        return cls.objects.filter(author__name__iendswith = 'a')

    @classmethod
    def books_with_given_author_and_publisher(cls, author, publisher):
        return cls.objects.filter(author = author, publisher = publisher)

    @classmethod
    def books_in_given_year(cls, year):
        return cls.objects.filter(date_of_pub__year = year)

    @staticmethod
    def get_date_of_pubs():
        return [date.today() - timedelta(days=x) for x in range(100)]

    @staticmethod
    def get_title():
        return "".join(random.choices(alphabets, k=50))

    @staticmethod
    def get_publishers():
        return list(Publisher.objects.all())

    @staticmethod
    def get_authors():
        return list(Author.objects.all())

    @classmethod
    def create_random_books(cls):
        authors = cls.get_authors()
        publishers = cls.get_publishers()
        dates = cls.get_date_of_pubs()

        for _ in range(50000):
            cls.objects.create(
            author = random.choice(authors),
            title = cls.get_title(),
            publisher = random.choice(publishers),
            date_of_pub = random.choice(dates)
        )

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        return super().save(**kwargs)
    
    def __str__(self):
        return self.title


class Collection(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    book = models.ManyToManyField(Book)

    @staticmethod
    def create_name():
        return "".join(random.choices(alphabets, k=8))
    
    @staticmethod
    def get_books():
        return list(Book.objects.all())

    @classmethod
    def create_random_collections(cls):
        books = cls.get_books()

        for _ in range(50000):
            collection = cls.objects.create(
            name = cls.create_name(),
        )
            collection.book.add(random.choice(books))

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)
    
    def __str__(self):
        return self.name
