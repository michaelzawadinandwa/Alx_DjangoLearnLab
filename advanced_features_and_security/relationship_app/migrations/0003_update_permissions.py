"""
Migration to update permissions for all models.
This migration adds comprehensive permissions for Author, Book, and Library models.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0002_alter_book_options_userprofile'),
    ]

    operations = [
        # Update Author model permissions
        migrations.AlterModelOptions(
            name='author',
            options={
                'permissions': [
                    ('can_view_author', 'Can view author'),
                    ('can_create_author', 'Can create author'),
                    ('can_edit_author', 'Can edit author'),
                    ('can_delete_author', 'Can delete author'),
                ]
            },
        ),
        # Update Book model permissions
        migrations.AlterModelOptions(
            name='book',
            options={
                'permissions': [
                    ('can_view', 'Can view a book'),
                    ('can_create', 'Can create a book'),
                    ('can_edit', 'Can edit a book'),
                    ('can_delete', 'Can delete a book'),
                    ('can_add_book', 'Can add a book'),
                    ('can_change_book', 'Can change a book'),
                    ('can_delete_book', 'Can delete a book'),
                ]
            },
        ),
        # Update Library model permissions
        migrations.AlterModelOptions(
            name='library',
            options={
                'permissions': [
                    ('can_view_library', 'Can view library'),
                    ('can_create_library', 'Can create library'),
                    ('can_edit_library', 'Can edit library'),
                    ('can_delete_library', 'Can delete library'),
                ]
            },
        ),
    ]
