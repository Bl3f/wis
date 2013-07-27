import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from web.apps.gallery.const import LARGE_FOLDER, MEDIUM_FOLDER, SMALL_FOLDER,\
    MEDIUM_WIDTH, MEDIUM_HEIGTH, SMALL_WIDTH, SMALL_HEIGHT


def get_upload_path(filename):
    # return os.path.join("user_%d" % instance.owner.id, "car_%s" % instance.slug, filename)
    return "pic/test/" + filename


class Document(models.Model):
    docfile = models.FileField(upload_to='pic/test')


class Photo(models.Model):
    large_path = models.ImageField(upload_to="upload/{}".format(LARGE_FOLDER))
    medium_path = models.CharField(max_length=255, blank=True)
    small_path = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=False)
    place = models.CharField(max_length=255, null=True)
    created = models.DateField(null=True)
    gallery = models.ForeignKey('Gallery', null=False)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        path = self.large_path.path
        image = Image.open(path)

        photo_extension = path.rsplit('/', 2)[2].rsplit('.', 1)[1]
        photo_name = path.rsplit('/', 2)[2].rsplit('.', 1)[0]
        abs_path = path.rsplit('/', 2)[0]

        image.resize((MEDIUM_WIDTH, MEDIUM_HEIGTH, Image.ANTIALIAS))
        image.save("{}/{}/{}-medium.{}".format(abs_path, MEDIUM_FOLDER, photo_name, photo_extension))

        image.thumbnail((SMALL_WIDTH, SMALL_HEIGHT, Image.ANTIALIAS))
        image.save("{}/{}/{}-small.{}".format(abs_path, SMALL_FOLDER, photo_name, photo_extension))


class GalleryManager(models.Manager):
    def get_galleries_with_slug(self):
        galleries = []
        for gallery in self.all():
            galleries.append({
                'owner': gallery.owner.username,
                'slug': gallery.slug_name,
                'name': gallery.title,
                'count': Photo.objects.filter(gallery=gallery).count(),
            })
        return galleries


class Gallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    slug_name = models.SlugField(max_length=255)
    public = models.BooleanField(default=True)
    owner = models.ForeignKey(User, null=False)
    place = models.CharField(max_length=255, null=True)
    created = models.DateField(null=True)
    objects = GalleryManager()

    def save(self, *args, **kwargs):
        if self.title:
            self.slug_name = slugify(self.title)[:255]
        super(Gallery, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
