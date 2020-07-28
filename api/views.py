from rest_framework import views, viewsets
from api.models import Book, Note, User
from api.serializers import BookSerializer, UserSerializer, NoteSerializer
from rest_framework import generics
from rest_framework import permissions
from api.permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers 
from rest_framework.generics import ListCreateAPIView
from rest_framework import filters

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(owner=user)

    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=status', 'author']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return None
        return Note.objects.filter(owner=user)

    serializer_class = NoteSerializer
    permissions_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(owner=user)

    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'notes': reverse('note-list', request=request, format=format),
    })