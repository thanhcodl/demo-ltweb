from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
import re
from unidecode import unidecode
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from .utils import unique_slug_generator

category_choices = {
    ('V-Pop', 'V-Pop'),
    ('K-Pop', 'K-Pop'),
    ('US-UK', 'US-UK')
}


class ModelMV(models.Model):
    name_MV = models.CharField(max_length=100, unique=True)
    name1_MV = models.CharField(max_length=100, blank=True)
    time_Post = models.DateTimeField(auto_now=True)
    author_MV = models.ForeignKey(User, on_delete=models.CASCADE)
    singer_MV = models.CharField(max_length=200)
    intro_MV = models.CharField(max_length=500)
    category_MV = models.CharField(choices=category_choices, max_length=10)
    description_MV = RichTextUploadingField()
    img_MV = models.ImageField(upload_to='img_mv/')
    link_Youtube = models.CharField(unique=True, max_length=500)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    view = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='mv_likes')

    def __str__(self):
        return self.name_MV

    # tên mv không dấu
    def save(self, *args, **kwargs):
        self.name1_MV = unidecode(self.name_MV)
        self.name_MV = self.name_MV.title()
        self.link_Youtube = re.sub('watch\?v=', 'embed/', self.link_Youtube)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mv:mv_detail_frontview', kwargs={'the_slug': self.slug})

    # đếm tổng số like
    def total_likes(self):
        return self.likes.all().count()


# Tạo slug
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=ModelMV)
