from django.db import models
import os


def get_upload_path(instance, filename):
    # return os.path.join("user_%d" % instance.owner.id, "car_%s" % instance.slug, filename)
    return "pic/test/" + filename


class Media(models.Model):
    owner_id = models.SmallIntegerField(null=True, blank=True, default=1)
    place = models.CharField(max_length=255, null=True)
    created = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


class Image(Media, models.Model):
    gallery = models.ForeignKey('Gallery', null=False)
    image = models.ImageField(upload_to=get_upload_path)
    uploaded = models.DateTimeField(auto_now_add=True)


class Gallery(Media, models.Model):
    title = models.CharField(max_length=255)
