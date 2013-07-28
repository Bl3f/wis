import time
import hashlib
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from web.apps.gallery.const import LARGE_FOLDER, MEDIUM_FOLDER, SMALL_FOLDER,\
    MEDIUM_WIDTH, MEDIUM_HEIGTH, SMALL_WIDTH, SMALL_HEIGHT, UPLOAD_FOLDER


def content_file_name(instance, filename):
    cypher = hashlib.new('sha512')

    photo_extension = filename.rsplit('.', 1)[1]
    cypher.update("{}{}{}".format(filename.rsplit('.', 1)[0], instance.owner.username, str(time.time())[:10]))
    instance.photo_hash = cypher.hexdigest()

    return '/'.join([UPLOAD_FOLDER, LARGE_FOLDER, "{}-large.{}".format(instance.photo_hash[:10], photo_extension)])


class Photo(models.Model):
    large_path = models.ImageField(upload_to=content_file_name)
    medium_path = models.CharField(max_length=255, blank=True)
    small_path = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=False)
    place = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateField(null=True)
    gallery = models.ForeignKey('Gallery', null=False)
    photo_hash = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        path = self.large_path.path
        image = Image.open(path)

        photo_extension = path.rsplit('/', 2)[2].rsplit('.', 1)[1]
        photo_name = self.photo_hash[:10]
        abs_path = path.rsplit('/', 3)[0]

        self.medium_path = '/'.join([UPLOAD_FOLDER, MEDIUM_FOLDER, "{}-medium.{}".format(photo_name, photo_extension)])
        image.thumbnail((MEDIUM_WIDTH, MEDIUM_HEIGTH), Image.ANTIALIAS)
        image.save('/'.join([abs_path, self.medium_path]))

        if image.size[0] <= image.size[1]:
            size = (SMALL_WIDTH, 'auto')
        else:
            size = ('auto', SMALL_HEIGHT)

        self.small_path = '/'.join([UPLOAD_FOLDER, SMALL_FOLDER, "{}-small.{}".format(photo_name, photo_extension)])
        image.thumbnail(size, Image.ANTIALIAS)
        image_width, image_height = image.size
        image = image.crop(((image_width - SMALL_WIDTH) / 2,
                            (image_height - SMALL_HEIGHT) / 2,
                            (image_width - SMALL_WIDTH) / 2 + SMALL_WIDTH,
                            (image_height - SMALL_HEIGHT) / 2 + SMALL_HEIGHT))
        image.save('/'.join([abs_path, self.small_path]))

        super(Photo, self).save(*args, **kwargs)


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
