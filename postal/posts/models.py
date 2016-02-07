#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import logging
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.db.models.signals import pre_delete
from django.conf import settings
from django.dispatch.dispatcher import receiver

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from taggit.managers import TaggableManager
from sorl import thumbnail as sorl_thumbnail

ZIP_TYPES = ['zip','7zip','rar']
WOTREPLAY = ['wotreplay']

logger = logging.getLogger(__name__)

def get_extension(filename):
    return os.path.splitext(filename)[-1]

def get_filename(filename):
    return os.path.basename(filename)

class FilePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, blank=True, auto_now_add=True)
    file = models.FileField(upload_to='files', blank=True)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, blank=True)
    tags = TaggableManager()

    @property
    def file_name(self):
        if self.file:
            return get_filename(self.file.name)
        else:
            return None

    @property
    def file_extension(self):
        if self.file:
            return get_extension(self.file.name)
        else:
            return None

    def get_thumbnail_url(self):
        if self.file:
            try:
                tn = sorl_thumbnail.get_thumbnail(self.file, '128x128', crop='center', quality=50)
                if tn.exists():
                    return tn.url
            except IOError:
                pass

        return None

class Post(TimeStampedModel, TitleSlugDescriptionModel):
    file = models.FileField(upload_to='posts', blank=True)
    image = sorl_thumbnail.ImageField(upload_to='posts', blank=True)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    tags = TaggableManager()

    @property
    def file_name(self):
        if self.file:
            return get_filename(self.file.name)
        else:
            return None

    @property
    def image_name(self):
        if self.image:
            return get_filename(self.image.name)
        else:
            return None

    def get_thumbnail_url(self):
        relative_url = None

        if self.image:
            try:
                relative_url = sorl_thumbnail.get_thumbnail(self.image, '64x64', crop='center', quality=99).url
            except IOError:
                pass

        elif self.file:
            try:
                extension = get_extension(self.file.path)[1:]
                static_url = '{static_url}img/filetypes/'.format(static_url=getattr(settings, 'STATIC_URL', '/static/'))

                if extension in WOTREPLAY:
                    relative_url = static_url + 'wot.png'

                elif extension in ZIP_TYPES:
                    relative_url = static_url + 'zip.png'

            except IOError:
                pass

        if relative_url:
            return relative_url

        return None

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=FilePost)
def filepost_delete(sender, instance, **kwargs):
    sorl_thumbnail.delete(instance.file, delete_file=False)
    
    # Delete post file
    instance.file.delete(False)

@receiver(pre_delete, sender=Post)
def post_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.

    # Delete post file
    instance.file.delete(False)

    if instance.image:
        # Delete post image and thumbnails
        sorl_thumbnail.delete(instance.image)
