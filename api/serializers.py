from rest_framework import serializers
from api.models import Book, Note, User


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    book_id = serializers.IntegerField()

    class Meta:
        model = Note
        fields = ['url', 'id', 'owner', 'book_id', 'body']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    notes = NoteSerializer(many=True, read_only=True)

    
    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'owner', 'notes', 'author', 'status']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only = True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'books']