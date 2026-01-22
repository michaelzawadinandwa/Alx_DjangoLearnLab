# Quick Start Guide

## Getting Started

### 1. Initial Setup
```bash
cd c:\Users\Admin\Alx_DjangoLearnLab-1\django-models
python manage.py migrate  # Already done, but included for reference
```

### 2. Create Admin User
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### 3. Run Development Server
```bash
python manage.py runserver
```

### 4. Create Sample Data (via Admin)

Visit: `http://localhost:8000/admin/`

**Step 1: Create Authors**
1. Go to Authors section
2. Click "Add Author"
3. Enter name (e.g., "J.K. Rowling", "George Orwell")
4. Save

**Step 2: Create Books**
1. Go to Books section
2. Click "Add Book"
3. Enter title and select author
4. Save

**Step 3: Create Libraries**
1. Go to Libraries section
2. Click "Add Library"
3. Enter name
4. Add books to library (use the ManyToMany field)
5. Save

**Step 4: Create Librarians**
1. Go to Librarians section
2. Click "Add Librarian"
3. Enter name and select library
4. Save

**Step 5: Create Users with Different Roles**
1. Go to Users section
2. Create new users (or use existing ones)
3. Go to User Profiles section
4. For each user, set their role:
   - Admin (for testing admin view)
   - Librarian (for testing librarian view)
   - Member (for testing member view)

### 5. Test the Application

#### Public Views (No Login Required)
- Books List: `http://localhost:8000/books/`
- Library Detail: `http://localhost:8000/library/1/` (replace 1 with library ID)

#### Authentication Views
- Register: `http://localhost:8000/register/`
- Login: `http://localhost:8000/login/`
- Logout: `http://localhost:8000/logout/`

#### Role-Based Views (Login Required)
- Admin Dashboard: `http://localhost:8000/admin/` (Admin users only)
- Librarian Dashboard: `http://localhost:8000/librarian/` (Librarian users only)
- Member Dashboard: `http://localhost:8000/member/` (Member users only)

#### Permission-Based Views (Login + Permission Required)
- Add Book: `http://localhost:8000/add-book/` (requires can_add_book permission)
- Edit Book: `http://localhost:8000/edit-book/1/` (requires can_change_book permission)
- Delete Book: `http://localhost:8000/delete-book/1/` (requires can_delete_book permission)

### 6. Assign Permissions to Users

Via Django Admin:

1. Go to Users section
2. Select a user
3. Go to "Permissions" section
4. Add the following permissions:
   - `relationship_app | book | Can add a book`
   - `relationship_app | book | Can change a book`
   - `relationship_app | book | Can delete a book`
5. Save

Or via Management Command:
```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

user = User.objects.get(username='username')
content_type = ContentType.objects.get_for_model(Book)
add_permission = Permission.objects.get(codename='can_add_book', content_type=content_type)
user.user_permissions.add(add_permission)
```

## Testing Workflows

### Workflow 1: Anonymous User Testing
1. Navigate to `http://localhost:8000/books/` without logging in
2. See list of books (public view)
3. Click on a library link to see library details
4. Try to access `http://localhost:8000/add-book/` → Should redirect to login

### Workflow 2: New User Registration
1. Go to `http://localhost:8000/register/`
2. Create new account (e.g., username: "testuser", password: "testpass123")
3. Auto-redirected to books page (auto-login after registration)
4. Auto-created UserProfile with default role "Member"
5. Try to access `http://localhost:8000/admin/` → Should get "Permission Denied"

### Workflow 3: Admin User Testing
1. Go to admin dashboard (logged in as Admin)
2. Access `http://localhost:8000/admin/` → Shows all users and their roles
3. Try to access `http://localhost:8000/member/` → Should get "Permission Denied"

### Workflow 4: Book Operations
1. Login as user with permissions
2. Go to `http://localhost:8000/add-book/`
3. Add a new book
4. Edit the book: `http://localhost:8000/edit-book/<book-id>/`
5. Delete the book: `http://localhost:8000/delete-book/<book-id>/`

### Workflow 5: Testing Permission Denial
1. Create user without book permissions
2. Login as that user
3. Try to access `http://localhost:8000/add-book/` → Should get "403 Forbidden"

## Files to Review

| File | Purpose |
|------|---------|
| `relationship_app/models.py` | All 5 models with relationships |
| `relationship_app/views.py` | All 15 views |
| `relationship_app/urls.py` | URL routing configuration |
| `relationship_app/admin.py` | Admin site customization |
| `relationship_app/query_samples.py` | ORM query examples |
| `LibraryProject/settings.py` | Project settings with app registration |
| `LibraryProject/urls.py` | Main URL configuration |

## Database Commands

```bash
# Create fresh migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Check project health
python manage.py check

# Create dump of data
python manage.py dumpdata > data_backup.json

# Load data from dump
python manage.py loaddata data_backup.json
```

## Troubleshooting

### Issue: "No module named 'relationship_app'"
**Solution**: Ensure 'relationship_app.apps.RelationshipAppConfig' is in INSTALLED_APPS in settings.py

### Issue: "Table relationship_app_userprofile does not exist"
**Solution**: Run `python manage.py migrate`

### Issue: Login redirect loops
**Solution**: Check LOGIN_REDIRECT_URL and LOGIN_URL in settings.py

### Issue: Templates not found
**Solution**: Ensure template directory structure is:
```
relationship_app/templates/relationship_app/[template_name].html
```

### Issue: CSRF token missing
**Solution**: Ensure `{% csrf_token %}` is included in all POST forms

## Performance Tips

1. Use select_related() for ForeignKey queries
2. Use prefetch_related() for ManyToMany queries
3. Add database indexes for frequently filtered fields
4. Cache role-based queries
5. Use pagination for large lists

## Security Reminders

- Never commit database file (db.sqlite3) to git
- Keep SECRET_KEY secret (use environment variables in production)
- Use HTTPS in production
- Set DEBUG = False in production
- Use environment variables for sensitive settings
- Regular security updates for Django and dependencies

## Next Steps

1. Add more models (Book Genres, Book Reviews, etc.)
2. Implement API endpoints with Django REST Framework
3. Add full-text search functionality
4. Implement book reservations system
5. Add email notifications
6. Deploy to production server
7. Set up CI/CD pipeline
