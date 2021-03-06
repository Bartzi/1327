# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-16 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='informationdocument',
            name='is_menu_page',
            field=models.BooleanField(default=False, help_text="Select this if the page is used mainly for navigation purposes and if all documents linked on the page should be removed from the 'unlinked information pages' list.", verbose_name='Is menu page'),
        ),
    ]
