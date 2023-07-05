from django.db import models
from django.conf import settings


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=202)
    phone = models.CharField(max_length=202)
    create_date = models.DateField(auto_now_add=True)
    is_view = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class About(models.Model):
    title = models.CharField(max_length=909)
    image = models.FileField(upload_to='abouts/')
    body = models.TextField()

    def __str__(self):
        return self.title

    @property
    def image_path(self):
        return f"{settings.SITE_URL}{self.image.url}"


class Goal(models.Model):
    icon = models.FileField(upload_to='goals/')
    title = models.CharField(max_length=202)
    body = models.TextField()

    def __str__(self):
        return self.title

    @property
    def icon_path(self):
        return f"{settings.SITE_URL}{self.icon.url}"
