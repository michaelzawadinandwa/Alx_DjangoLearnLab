from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with custom fields.
    Ensures that create_user and create_superuser methods work properly
    with the new custom fields (date_of_birth and profile_photo).
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        
        Args:
            email: User's email address (used as username)
            password: User's password
            **extra_fields: Additional fields like username, date_of_birth, profile_photo
        
        Returns:
            CustomUser: The created user instance
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        Ensures that is_staff and is_superuser are set to True.
        
        Args:
            email: Superuser's email address
            password: Superuser's password
            **extra_fields: Additional fields
        
        Returns:
            CustomUser: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with additional fields.
    
    Additional Fields:
    - date_of_birth: User's date of birth (optional)
    - profile_photo: User's profile photo (optional image file)
    
    This model replaces Django's default User model and allows for custom
    user attributes specific to the application's needs.
    """
    
    email = models.EmailField(unique=True, max_length=255)
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile photo"
    )
    
    # Use email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'accounts_customuser'

    def __str__(self):
        return f"{self.username} ({self.email})"

    def get_full_name(self):
        """
        Return the user's full name or email if full name is not available.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email
