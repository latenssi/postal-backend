from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from .models import FilePost, Post
from postal.user.serializers import UserSerializer

class FilePostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField(required=False)
    user = UserSerializer(read_only=True)
    file_name = serializers.CharField(read_only=True)
    file_extension = serializers.CharField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = FilePost
        read_only_fields = ('id', 'user')
        depth = 1

    def get_thumbnail_url(self, obj):
        thumbnail_url = obj.get_thumbnail_url()
        if thumbnail_url:
            return self.context['view'].request.build_absolute_uri(thumbnail_url)
        return None

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    file_name = serializers.CharField(read_only=True)
    image_name = serializers.CharField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        read_only_fields = ('id', 'user')
        depth = 1

    def get_thumbnail_url(self, obj):
        thumbnail_url = obj.get_thumbnail_url()
        if thumbnail_url:
            return self.context['view'].request.build_absolute_uri(thumbnail_url)
        return None
