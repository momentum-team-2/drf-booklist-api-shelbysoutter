from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Q
from django.contrib.postgres.search import SearchVector


class User(AbstractUser):
    pass


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    status = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title}: {self.author}"


class Note(models.Model):
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes', null=True)
    created = models.DateTimeField(auto_now_add=True)


def get_book(queryset, user):
    if user.is_authenticated:
        books = queryset.filter(Q(owner=user))
    return books


def search_books(user, search_term):
    books = get_book(Book.objects, user)
    books = books.annotate(search=SearchVector(
        'title', 'author'
    ))
    books = books.filter(search=search_term).distinct('pk')
    return books