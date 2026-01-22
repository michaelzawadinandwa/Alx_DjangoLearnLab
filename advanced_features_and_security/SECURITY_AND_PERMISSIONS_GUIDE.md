# Advanced Django Features and Security Documentation

## Overview

This project demonstrates advanced Django features including custom user models, permission-based access control, and security best practices.

## Table of Contents

1. [Custom User Model](#custom-user-model)
2. [Permissions and Groups](#permissions-and-groups)
3. [Security Best Practices](#security-best-practices)
4. [HTTPS and Secure Headers](#https-and-secure-headers)
5. [Setup Instructions](#setup-instructions)

---

## Custom User Model

### Overview

This project replaces Django's default user model with a custom user model (`CustomUser`) that extends `AbstractUser` with additional fields relevant to the application.

### Additional Fields

- **date_of_birth** (DateField): Optional field for storing the user's date of birth
- **profile_photo** (ImageField): Optional field for storing the user's profile photo

### Custom User Manager

The `CustomUserManager` class handles user creation:

- **create_user(email, password, **extra_fields)**: Creates a regular user with email as the unique identifier
- **create_superuser(email, password, **extra_fields)**: Creates a superuser with proper permissions

### Configuration

In `settings.py`:
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Admin Integration

The custom user model is integrated into Django Admin through `CustomUserAdmin` class:
- Display custom fields in the admin list view
- Organize fields into logical sections (Personal Info, Permissions, Important Dates)
- Filter horizontal display for many-to-many relationships

---

## Permissions and Groups

### Overview

The system implements granular access control using Django's permission and group system. This allows administrators to assign specific permissions to users or groups, controlling who can perform certain actions.

### Custom Permissions

Permissions are defined in model `Meta` classes:

#### Book Model Permissions
- **can_view**: Can view a book
- **can_create**: Can create a book
- **can_edit**: Can edit a book
- **can_delete**: Can delete a book
- **can_add_book**: Can add a book (legacy)
- **can_change_book**: Can change a book (legacy)
- **can_delete_book**: Can delete a book (legacy)

#### Author Model Permissions
- **can_view_author**: Can view author
- **can_create_author**: Can create author
- **can_edit_author**: Can edit author
- **can_delete_author**: Can delete author

#### Library Model Permissions
- **can_view_library**: Can view library
- **can_create_library**: Can create library
- **can_edit_library**: Can edit library
- **can_delete_library**: Can delete library

### Predefined Groups

Administrators should create the following groups in Django Admin:

#### Editors Group
**Permissions:**
- `relationship_app.can_add_book`
- `relationship_app.can_edit` or `relationship_app.can_change_book`

**Capabilities:**
- Create new books
- Edit existing books
- View the book list

#### Viewers Group
**Permissions:**
- `relationship_app.can_view`

**Capabilities:**
- View books
- View book details
- No modification capabilities

#### Admins Group
**Permissions:**
- `relationship_app.can_add_book`
- `relationship_app.can_edit`
- `relationship_app.can_delete`
- All other admin permissions

**Capabilities:**
- Full CRUD operations on books
- Manage users and permissions
- Access admin dashboard

### Role-Based Access Control

In addition to permissions, the system uses role-based access control through the `UserProfile` model:

**Roles:**
- **Admin**: Full system access
- **Librarian**: Can manage library inventory
- **Member**: Regular user with limited access

**Usage in Views:**
```python
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view(request):
    # Only accessible to Admin role users
    pass
```

### Using Permissions in Views

Protect views with permission decorators:

```python
@login_required(login_url='login')
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    # Only users with can_edit permission can access
    pass
```

### Setting Up Permissions and Groups

1. Create superuser: `python manage.py createsuperuser`
2. Run migrations: `python manage.py migrate`
3. Access Django Admin: `/admin/`
4. Create groups and assign permissions through the admin interface
5. Assign users to groups

---

## Security Best Practices

### 1. DEBUG Setting

**In settings.py:**
```python
DEBUG = False  # Always set to False in production
```

**Why:** Disabling DEBUG prevents the exposure of sensitive information like settings, stack traces, and file paths in error pages.

### 2. XSS (Cross-Site Scripting) Protection

**Settings:**
```python
SECURE_BROWSER_XSS_FILTER = True
```

**Implementation in Views:**
```python
from django.utils.html import escape

def sanitize_input(value):
    """Escape HTML characters to prevent XSS"""
    return escape(value) if value else None
```

**In Templates:**
```html
<!-- Django auto-escapes by default -->
{{ user_input }}  <!-- Safe - Django escapes HTML -->
```

### 3. CSRF (Cross-Site Request Forgery) Protection

**Settings:**
```python
CSRF_COOKIE_SECURE = True        # Only send over HTTPS
CSRF_COOKIE_HTTPONLY = True      # Prevent JavaScript access
```

**In Templates:**
```html
<form method="post">
    {% csrf_token %}  <!-- Required in all forms -->
    <!-- form fields -->
</form>
```

**In Views:**
```python
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def protected_view(request):
    pass
```

### 4. MIME-Type Sniffing Protection

**Settings:**
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Why:** Prevents browsers from MIME-sniffing response content away from the declared content-type, protecting against certain attacks.

### 5. Clickjacking Protection

**Settings:**
```python
X_FRAME_OPTIONS = 'DENY'
```

**Why:** Prevents your site from being framed by other sites, protecting against clickjacking attacks.

### 6. Session Security

**Settings:**
```python
SESSION_COOKIE_SECURE = True      # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True    # Prevent JavaScript access
```

### 7. SQL Injection Prevention

**Safe (using Django ORM):**
```python
# Always use Django ORM to prevent SQL injection
book = Book.objects.get(id=book_id)
books = Book.objects.filter(title=search_term)
```

**Unsafe (avoid):**
```python
# Never use raw SQL with string formatting
query = f"SELECT * FROM book WHERE id = {user_input}"  # VULNERABLE!
```

### 8. Input Validation

**Best Practices:**
```python
# Always validate and sanitize user input
username = request.POST.get('username', '').strip()
username = sanitize_input(username)

# Validate in Django forms
class MyForm(forms.Form):
    email = forms.EmailField()  # Validates email format
    age = forms.IntegerField(min_value=0, max_value=120)
```

---

## HTTPS and Secure Headers

### 1. SSL/TLS Configuration

**Settings:**
```python
# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True  # Set to False in development

# HTTP Strict-Transport-Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Why:** 
- Ensures all traffic is encrypted
- Tells browsers to always use HTTPS for your site
- Prevents downgrade attacks

### 2. Secure Cookies

**Settings:**
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Why:** Ensures cookies are only transmitted over HTTPS connections.

### 3. Security Headers

**Configured Headers:**

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Frame-Options` | `DENY` | Prevents clickjacking |
| `X-Content-Type-Options` | `nosniff` | Prevents MIME sniffing |
| `X-XSS-Protection` | Enabled | Browser XSS filtering |

### 4. Deployment Configuration

For production deployment with Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL certificates
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Redirect HTTP to HTTPS
    error_page 497 https://$server_name$request_uri;
    
    # Django configuration
    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Setup Instructions

### 1. Initial Setup

```bash
# Clone the repository
cd advanced_features_and_security

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create migrations for new custom user model
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser (for the custom user model)
python manage.py createsuperuser

# Create groups and assign permissions (in Django Admin)
python manage.py shell
```

### 2. Create Groups in Django Shell

```python
from django.contrib.auth.models import Group, Permission
from relationship_app.models import Book

# Create groups
editors_group, _ = Group.objects.get_or_create(name='Editors')
viewers_group, _ = Group.objects.get_or_create(name='Viewers')
admins_group, _ = Group.objects.get_or_create(name='Admins')

# Get permissions
can_add = Permission.objects.get(codename='can_add_book')
can_edit = Permission.objects.get(codename='can_edit')
can_delete = Permission.objects.get(codename='can_delete')

# Assign permissions to groups
editors_group.permissions.add(can_add, can_edit)
viewers_group.permissions.add(can_add)
admins_group.permissions.add(can_add, can_edit, can_delete)

print("Groups created successfully!")
```

### 3. Run Development Server

```bash
# Development (DEBUG=False for testing security features)
python manage.py runserver

# Access the application at http://localhost:8000
```

### 4. Testing

- Create test users in Django Admin
- Assign users to different groups
- Log in as different users
- Test access to protected views (add, edit, delete)
- Verify permission checks are working

### 5. Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Set up SSL/TLS certificates
4. Configure `SECURE_SSL_REDIRECT = True`
5. Configure web server (Nginx/Apache) with security headers
6. Use environment variables for sensitive settings
7. Set up database backups
8. Configure logging and monitoring

---

## Security Checklist

- [x] DEBUG set to False
- [x] CSRF tokens in all forms
- [x] XSS protection enabled
- [x] MIME-sniffing protection enabled
- [x] Clickjacking protection enabled
- [x] Session cookies secure (HTTPS only)
- [x] Input validation and sanitization
- [x] Django ORM used for database queries
- [x] Permission checks in views
- [x] HSTS headers configured
- [x] Custom user model implemented
- [x] Permissions and groups configured

---

## References

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Permissions and Groups](https://docs.djangoproject.com/en/stable/topics/auth/)
- [Django Custom User Model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)
