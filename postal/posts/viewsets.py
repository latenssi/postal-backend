from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from postal.permissions import IsOwnerOrReadOnly
from .models import FilePost, Post
from .serializers import FilePostSerializer, PostSerializer

class FilePostViewSet(viewsets.ModelViewSet):
    serializer_class = FilePostSerializer
    queryset = FilePost.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
