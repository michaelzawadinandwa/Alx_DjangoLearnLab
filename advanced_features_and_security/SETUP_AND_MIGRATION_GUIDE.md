# Setup and Migration Guide

## Initial Setup

### 1. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
# Create initial migrations
python manage.py makemigrations

# Apply all migrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

When prompted, use the custom user model:
- Email: admin@example.com
- Username: admin
- Password: (your password)
- Date of Birth: (optional)

### 5. Create Test Data

Run the following commands to set up test data:

```bash
python manage.py shell
```

Then execute:

```python
from django.contrib.auth.models import Group, Permission
from accounts.models import CustomUser
from relationship_app.models import Author, UserProfile

# Create groups
editors, _ = Group.objects.get_or_create(name='Editors')
viewers, _ = Group.objects.get_or_create(name='Viewers')
admins, _ = Group.objects.get_or_create(name='Admins')

# Get permissions
try:
    can_add = Permission.objects.get(codename='can_add_book')
    can_edit = Permission.objects.get(codename='can_edit')
    can_delete = Permission.objects.get(codename='can_delete')
    
    # Assign permissions to groups
    editors.permissions.set([can_add, can_edit])
    viewers.permissions.set([can_add])
    admins.permissions.set([can_add, can_edit, can_delete])
    
    print("✓ Groups created successfully!")
except Exception as e:
    print(f"Note: Permissions may not be available yet. Run migrations if needed.")
    print(f"Error: {e}")

# Create test authors
Author.objects.get_or_create(name='George Orwell')
Author.objects.get_or_create(name='J.K. Rowling')
Author.objects.get_or_create(name='Stephen King')

print("✓ Test authors created!")
exit()
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Access the application at:
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Database Operations

### Create Migrations for Model Changes

```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Rollback Migrations

```bash
# Rollback to previous migration
python manage.py migrate relationship_app 0002

# Reset app
python manage.py migrate relationship_app zero
```

### View Migration Status

```bash
python manage.py showmigrations
```

## Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific App Tests

```bash
python manage.py test relationship_app
python manage.py test accounts
```

### Run with Verbose Output

```bash
python manage.py test --verbosity=2
```

## Admin Operations

### Create Superuser from Command Line

```bash
python manage.py createsuperuser
```

### Change User Password

```bash
python manage.py changepassword username
```

### Create User from Shell

```bash
python manage.py shell

from accounts.models import CustomUser

user = CustomUser.objects.create_user(
    email='user@example.com',
    username='testuser',
    password='testpass123',
    date_of_birth='1990-01-15',
)
print(f"User {user.username} created successfully!")
exit()
```

## Troubleshooting

### Migration Errors

If you encounter migration errors:

```bash
# Remove migration files (be careful!)
# Then run:
python manage.py makemigrations --empty relationship_app --name fix_migrations
python manage.py migrate
```

### Database Locked

If you get "database is locked" errors:

```bash
# Delete the database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Import Errors

If you get import errors after changing settings:

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

## Production Deployment

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Run with Gunicorn

```bash
gunicorn LibraryProject.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables (Create .env file)

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Useful Django Commands

```bash
# Start interactive Python shell with Django context
python manage.py shell

# Check for issues
python manage.py check

# See all installed apps
python manage.py shell -c "from django.conf import settings; print('\n'.join(settings.INSTALLED_APPS))"

# Get database schema information
python manage.py sqlmigrate relationship_app 0001

# Print SQL for a model
python manage.py sqlmigrate relationship_app 0002
```

## Creating Fixtures for Testing

```bash
# Export data
python manage.py dumpdata relationship_app > relationship_app_fixture.json

# Load data
python manage.py loaddata relationship_app_fixture.json
```

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Custom User Model: https://docs.djangoproject.com/en/stable/topics/auth/customizing/
- Permissions and Groups: https://docs.djangoproject.com/en/stable/topics/auth/
- Security: https://docs.djangoproject.com/en/stable/topics/security/
