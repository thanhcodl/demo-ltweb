# Generated by Django 3.0.8 on 2020-07-31 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Giới tính thứ ba', 'Giới tính thứ ba')], default='Nam', max_length=20, null=True),
        ),
    ]