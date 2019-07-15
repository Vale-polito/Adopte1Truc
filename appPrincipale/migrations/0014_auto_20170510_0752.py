# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-10 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPrincipale', '0013_objet_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objet',
            name='image',
        ),
        migrations.AddField(
            model_name='objet',
            name='photo',
            field=models.ImageField(default='ryan.jpg', upload_to='photos/'),
        ),
    ]