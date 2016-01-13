from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from .models import Post
from postal.user.serializers import UserSerializer

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    file_name = serializers.CharField(read_only=True)
    image_name = serializers.CharField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        # fields = ('id', 'title', 'slug', 'user', 'tags')
        read_only_fields = ('id', 'user')
        depth = 1

    def get_thumbnail_url(self, obj):
        thumbnail_url = obj.get_thumbnail_url()
        if thumbnail_url:
            return self.context['view'].request.build_absolute_uri(obj.get_thumbnail_url())
        return None
