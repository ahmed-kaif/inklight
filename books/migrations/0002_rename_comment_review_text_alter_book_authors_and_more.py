# Generated by Django 5.0.1 on 2024-03-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='comment',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(blank=True, to='books.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
