# Advanced Features and Security - Django Learning Lab

## Overview

This project demonstrates advanced Django features and security best practices, including:

1. **Custom User Model** - Extending Django's authentication system with additional fields
2. **Permissions and Groups** - Role-based access control and granular permissions
3. **Security Best Practices** - Protection against common web vulnerabilities
4. **HTTPS and Secure Headers** - Secure communication and defense against attacks

## Quick Start

### Prerequisites
- Python 3.8+
- Django 6.0+
- Virtual environment (recommended)

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

Access the application:
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Project Structure

```
advanced_features_and_security/
├── accounts/                          # Custom user model app
│   ├── models.py                      # CustomUser and CustomUserManager
│   ├── admin.py                       # CustomUserAdmin configuration
│   ├── apps.py
│   └── migrations/
│
├── relationship_app/                  # Main application with permissions
│   ├── models.py                      # Book, Author, Library models with permissions
│   ├── views.py                       # Permission-protected views
│   ├── admin.py
│   ├── urls.py
│   └── templates/                     # HTML templates with CSRF tokens
│       └── relationship_app/
│           ├── login.html
│           ├── register.html
│           ├── add_book.html
│           ├── edit_book.html
│           └── delete_book.html
│
├── bookshelf/                         # Book management app
├── LibraryProject/
│   ├── settings.py                    # Security configurations
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt
```

## Features Implemented

### 1. Custom User Model ✅

**Location:** `accounts/models.py`

- Extended `AbstractUser` with:
  - `date_of_birth` field
  - `profile_photo` field
- Custom user manager handling user creation
- Configured in settings with `AUTH_USER_MODEL = 'accounts.CustomUser'`

**Admin Integration:**
- Custom admin class in `accounts/admin.py`
- Special fieldsets for custom fields
- Search and filter capabilities

### 2. Permissions and Groups ✅

**Location:** `relationship_app/models.py` and `views.py`

**Permissions Defined:**
- **Book:** can_view, can_create, can_edit, can_delete
- **Author:** can_view_author, can_create_author, can_edit_author, can_delete_author
- **Library:** can_view_library, can_create_library, can_edit_library, can_delete_library

**Predefined Groups:**
- **Editors** - can_add_book, can_edit
- **Viewers** - can_view
- **Admins** - All permissions

**Protected Views:**
```python
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    # Only users with can_edit permission
    pass
```

**Role-Based Access Control:**
- Admin Dashboard - Only Admin role users
- Librarian Dashboard - Only Librarian role users
- Member Dashboard - Only Member role users

### 3. Security Best Practices ✅

**Location:** `LibraryProject/settings.py` and `relationship_app/views.py`

**Configured Security Settings:**
- ✅ DEBUG = False (production-ready)
- ✅ SECURE_BROWSER_XSS_FILTER = True
- ✅ SECURE_CONTENT_TYPE_NOSNIFF = True
- ✅ X_FRAME_OPTIONS = 'DENY'
- ✅ CSRF_COOKIE_SECURE = True
- ✅ CSRF_COOKIE_HTTPONLY = True
- ✅ SESSION_COOKIE_SECURE = True
- ✅ SESSION_COOKIE_HTTPONLY = True

**Implemented Protections:**
- XSS Prevention: Input escaping and auto-escaping templates
- CSRF Protection: CSRF tokens in all forms ({% csrf_token %})
- SQL Injection Prevention: Django ORM for all queries
- Input Validation: Form validation and sanitization

### 4. HTTPS and Secure Headers ✅

**Location:** `LibraryProject/settings.py`

**HTTPS Configuration:**
- SECURE_SSL_REDIRECT = False (set to True in production)
- SECURE_HSTS_SECONDS = 31536000 (1 year)
- SECURE_HSTS_INCLUDE_SUBDOMAINS = True
- SECURE_HSTS_PRELOAD = True

**Security Headers:**
- X-Frame-Options: DENY (Clickjacking protection)
- X-Content-Type-Options: nosniff (MIME-sniffing protection)
- X-XSS-Protection: Enabled (Browser XSS filtering)

## Documentation

### Main Guides
- **[SECURITY_AND_PERMISSIONS_GUIDE.md](./SECURITY_AND_PERMISSIONS_GUIDE.md)** - Comprehensive security documentation
- **[SETUP_AND_MIGRATION_GUIDE.md](./SETUP_AND_MIGRATION_GUIDE.md)** - Setup instructions and database management
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - Testing procedures and troubleshooting

## Usage Examples

### 1. Creating Users via Admin

1. Go to `/admin/`
2. Navigate to Users > Add User
3. Enter custom fields:
   - Date of Birth
   - Profile Photo
4. Save

### 2. Setting Up Permissions

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group, Permission

# Create group
editors, _ = Group.objects.get_or_create(name='Editors')

# Get permissions
can_edit = Permission.objects.get(codename='can_edit')
can_add = Permission.objects.get(codename='can_add_book')

# Assign permissions
editors.permissions.add(can_edit, can_add)
```

### 3. Assigning Users to Groups

```python
user.groups.add(editors)  # Add to group
user.groups.remove(viewers)  # Remove from group
user.groups.clear()  # Remove all groups
```

### 4. Checking User Permissions

```python
user.has_perm('relationship_app.can_edit')  # Check single permission
user.get_all_permissions()  # Get all permissions
user.groups.all()  # Get user's groups
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

### Manual Testing
Follow the comprehensive testing guide in [TESTING_GUIDE.md](./TESTING_GUIDE.md)

## Security Checklist

- [x] DEBUG set to False
- [x] CSRF tokens in all forms
- [x] XSS protection enabled
- [x] MIME-sniffing protection enabled
- [x] Clickjacking protection enabled
- [x] Session cookies secure
- [x] Input validation and sanitization
- [x] Django ORM used for queries
- [x] Permission checks in views
- [x] HSTS headers configured
- [x] Custom user model implemented
- [x] Permissions and groups configured

## Key Files

| File | Purpose |
|------|---------|
| `accounts/models.py` | CustomUser model and manager |
| `accounts/admin.py` | Admin configuration for custom user |
| `relationship_app/models.py` | Models with permissions and signals |
| `relationship_app/views.py` | Views with permission checks and security |
| `LibraryProject/settings.py` | Security configurations |
| `SECURITY_AND_PERMISSIONS_GUIDE.md` | Detailed security documentation |
| `SETUP_AND_MIGRATION_GUIDE.md` | Setup and management guide |
| `TESTING_GUIDE.md` | Testing procedures |

## API Endpoints

### Authentication
- `GET /relationship_app/login/` - Login page
- `POST /relationship_app/login/` - Login submission
- `GET /relationship_app/register/` - Registration page
- `POST /relationship_app/register/` - Registration submission
- `GET /relationship_app/logout/` - Logout

### Main Functionality
- `GET /relationship_app/list_books/` - List all books
- `GET /relationship_app/library/<id>/` - Library details
- `GET/POST /relationship_app/add_book/` - Add book (requires permission)
- `GET/POST /relationship_app/edit_book/<id>/` - Edit book (requires permission)
- `GET/POST /relationship_app/delete_book/<id>/` - Delete book (requires permission)

### Dashboard Views
- `GET /relationship_app/admin_view/` - Admin dashboard (Admin role only)
- `GET /relationship_app/librarian_view/` - Librarian dashboard (Librarian role only)
- `GET /relationship_app/member_view/` - Member dashboard (Member role only)

## Deployment

### Production Settings
1. Set DEBUG = False
2. Configure ALLOWED_HOSTS with your domain
3. Set SECURE_SSL_REDIRECT = True
4. Use environment variables for SECRET_KEY
5. Configure database with PostgreSQL
6. Collect static files: `python manage.py collectstatic`
7. Use Gunicorn as WSGI server
8. Configure Nginx/Apache with SSL

### Environment Variables
Create `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
SECURE_SSL_REDIRECT=True
```

## Technologies Used

- Django 6.0
- Python 3.8+
- SQLite (development) / PostgreSQL (production)
- Pillow (for image handling)
- Gunicorn (production server)

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Custom User Models](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)
- [Permissions and Groups](https://docs.djangoproject.com/en/stable/topics/auth/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Contributing

This project is part of the ALX Django Learning Lab. Follow these steps to contribute:

1. Create a feature branch
2. Make changes following Django best practices
3. Test thoroughly
4. Submit a pull request

## License

This project is for educational purposes.

## Support

For issues or questions:
1. Check the documentation files
2. Review the testing guide
3. Consult Django official documentation
4. Check the OWASP security guidelines

---

**Last Updated:** January 2026
**Django Version:** 6.0
**Status:** ✅ All features implemented and tested
