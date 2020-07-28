from rest_framework import serializers
from api.models import Book, Note, User

class NestedNoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ['body']


class NestedBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['title']


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page_number = serializers.IntegerField()
    created = serializers.DateTimeField()
    #book = NestedBookSerializer()

    class Meta:
        model = Note
        fields = ['url', 'id', 'owner', 'body', 'book', 'page_number', 'created']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    notes = NestedNoteSerializer(many=True)
    
    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'owner', 'author', 'status', 'notes']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only = True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'books']