from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    file_name = serializers.CharField(read_only=True)
    image_name = serializers.CharField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = ('id', 'title', 'slug', 'user', 'tags')
        read_only_fields = ('id', 'user')

    def get_thumbnail_url(self, obj):
        return self.context['view'].request.build_absolute_uri(obj.get_thumbnail_url())
