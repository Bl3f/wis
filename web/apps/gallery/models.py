from django.db import models
from django.template.defaultfilters import slugify
import os


def get_upload_path(filename):
    # return os.path.join("user_%d" % instance.owner.id, "car_%s" % instance.slug, filename)
    return "pic/test/" + filename


class Document(models.Model):
    docfile = models.FileField(upload_to='pic/test')


class Image(models.Model):
    path = models.ImageField(upload_to="upload")# get_upload_path)
    description = models.CharField(max_length=255, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    owner_id = models.SmallIntegerField(null=True, blank=True, default=1)
    place = models.CharField(max_length=255, null=True)
    created = models.DateField(null=True)
    gallery = models.ForeignKey('Gallery', null=False)


class Gallery(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    slug_name = models.SlugField(max_length=255)
    public = models.BooleanField(default=True)
    owner_id = models.SmallIntegerField(null=True, blank=True, default=1)
    place = models.CharField(max_length=255, null=True)
    created = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if self.title:
            self.slug_name = slugify(self.title)[:255]
        super(Gallery, self).save(*args, **kwargs)