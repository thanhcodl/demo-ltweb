# Generated by Django 3.0.8 on 2020-07-31 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default='/profiles_pic/default_pic.jpg', null=True, upload_to='profiles_pic')),
                ('gender', models.CharField(blank=True, choices=[('Nữ', 'Nữ'), ('Nam', 'Nam'), ('Giới tính thứ ba', 'Giới tính thứ ba')], default='Nam', max_length=20, null=True)),
                ('time_join', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
