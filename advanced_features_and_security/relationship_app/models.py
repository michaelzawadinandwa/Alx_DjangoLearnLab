from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    """Model to represent an Author"""
    name = models.CharField(max_length=100)
    
    class Meta:
        permissions = [
            ('can_view_author', 'Can view author'),
            ('can_create_author', 'Can create author'),
            ('can_edit_author', 'Can edit author'),
            ('can_delete_author', 'Can delete author'),
        ]
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Model to represent a Book with custom permissions for access control"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        # Custom permissions for granular access control
        # These permissions can be assigned to groups and users
        permissions = [
            ('can_view', 'Can view a book'),
            ('can_create', 'Can create a book'),
            ('can_edit', 'Can edit a book'),
            ('can_delete', 'Can delete a book'),
            ('can_add_book', 'Can add a book'),
            ('can_change_book', 'Can change a book'),
            ('can_delete_book', 'Can delete a book'),
        ]
    
    def __str__(self):
        return self.title


class Library(models.Model):
    """Model to represent a Library"""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    class Meta:
        permissions = [
            ('can_view_library', 'Can view library'),
            ('can_create_library', 'Can create library'),
            ('can_edit_library', 'Can edit library'),
            ('can_delete_library', 'Can delete library'),
        ]
    
    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Model to represent a Librarian"""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended User Profile with role-based access control"""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    # Use the custom user model instead of the default User
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Signal to automatically create UserProfile when a new custom user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a UserProfile whenever a new user is created.
    This ensures every user automatically has an associated profile.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the UserProfile whenever the user is saved.
    This ensures profile changes are persisted when user is updated.
    """
    instance.userprofile.save()

