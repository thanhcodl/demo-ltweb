from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

gender_choices = {
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ'),
    ('Giới tính thứ ba', 'Giới tính thứ ba'),
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='profiles_pic', blank=True, null=True, default='/profiles_pic/default_pic.jpg')
    gender = models.CharField(choices=gender_choices, blank=True, max_length=20, null=True, default='Nam')
    time_join = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
