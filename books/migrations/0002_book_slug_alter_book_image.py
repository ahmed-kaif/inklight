# Generated by Django 5.0.1 on 2024-03-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
