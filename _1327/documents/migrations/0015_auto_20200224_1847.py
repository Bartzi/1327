# Generated by Django 2.2.9 on 2020-02-24 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_merge_20191118_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='text_de',
            field=models.TextField(blank=True, verbose_name='Text (German)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='text_en',
            field=models.TextField(blank=True, verbose_name='Text (English)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title_de',
            field=models.CharField(max_length=255, verbose_name='Title (German)'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title_en',
            field=models.CharField(max_length=255, verbose_name='Title (English)'),
        ),
    ]