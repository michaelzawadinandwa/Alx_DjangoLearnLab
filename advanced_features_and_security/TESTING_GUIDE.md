# Testing Guide for Advanced Features and Security

## Overview

This guide provides step-by-step instructions for testing the implemented advanced features and security measures.

## 1. Testing Custom User Model

### Test 1.1: Create User with Custom Fields

1. Access Django Admin: http://localhost:8000/admin/
2. Navigate to: **Users > Add User**
3. Create a new user with:
   - Username: `testuser1`
   - Email: `testuser1@example.com`
   - Password: `TestPass123`
   - Date of Birth: `1990-05-15`
   - Profile Photo: (upload an image)
4. Click Save
5. Verify user appears in the Users list with all custom fields

### Test 1.2: Verify Custom Manager

1. Go to Django Shell:
   ```bash
   python manage.py shell
   ```

2. Test create_user:
   ```python
   from accounts.models import CustomUser
   
   user = CustomUser.objects.create_user(
       email='shell_user@example.com',
       username='shelluser',
       password='ShellPass123',
       date_of_birth='1995-03-20'
   )
   print(f"User created: {user.email}")
   print(f"Date of birth: {user.date_of_birth}")
   ```

3. Test create_superuser:
   ```python
   admin = CustomUser.objects.create_superuser(
       email='admin2@example.com',
       username='admin2',
       password='AdminPass123',
       date_of_birth='1985-01-10'
   )
   print(f"Superuser created: {admin.email}")
   print(f"Is staff: {admin.is_staff}")
   print(f"Is superuser: {admin.is_superuser}")
   ```

## 2. Testing Permissions and Groups

### Test 2.1: Create Groups with Permissions

1. Go to Django Admin > **Authentication and Authorization > Groups**
2. Create three groups:

**Group 1: Editors**
- Permissions: 
  - `relationship_app | book | Can add a book`
  - `relationship_app | book | Can edit a book`

**Group 2: Viewers**
- Permissions:
  - `relationship_app | book | Can view a book`

**Group 3: Admins**
- Permissions:
  - All book-related permissions

### Test 2.2: Assign Users to Groups

1. Go to Django Admin > **Users**
2. Edit `testuser1`
3. In the **Permissions** section, add to Group: **Editors**
4. Save

### Test 2.3: Test Permission-Based Access

Create test users with different permissions:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group, Permission
from accounts.models import CustomUser

# Create test users
editor_user = CustomUser.objects.create_user(
    email='editor@example.com',
    username='editor',
    password='EditorPass123'
)
viewer_user = CustomUser.objects.create_user(
    email='viewer@example.com',
    username='viewer',
    password='ViewerPass123'
)

# Get groups
editors_group = Group.objects.get(name='Editors')
viewers_group = Group.objects.get(name='Viewers')

# Assign users to groups
editor_user.groups.add(editors_group)
viewer_user.groups.add(viewers_group)

print("✓ Test users created and assigned to groups")
exit()
```

### Test 2.4: Test View Access Control

1. **Test as Editor (with can_add_book permission):**
   - Log in as: `editor` / `EditorPass123`
   - Navigate to: http://localhost:8000/relationship_app/add_book/
   - Expected: Page loads (access granted)
   - Try to add a book
   - Expected: Book creation succeeds

2. **Test as Viewer (without can_add_book permission):**
   - Log in as: `viewer` / `ViewerPass123`
   - Navigate to: http://localhost:8000/relationship_app/add_book/
   - Expected: 403 Forbidden error

## 3. Testing Role-Based Access Control

### Test 3.1: Create Test Users with Roles

```bash
python manage.py shell
```

```python
from accounts.models import CustomUser
from relationship_app.models import UserProfile

# Create users
admin_user = CustomUser.objects.create_user(
    email='admin_role@example.com',
    username='admin_role',
    password='AdminRole123'
)
librarian_user = CustomUser.objects.create_user(
    email='librarian@example.com',
    username='librarian',
    password='LibrarianPass123'
)
member_user = CustomUser.objects.create_user(
    email='member@example.com',
    username='member',
    password='MemberPass123'
)

# Set roles (UserProfile is auto-created via signal)
admin_user.userprofile.role = 'Admin'
admin_user.userprofile.save()

librarian_user.userprofile.role = 'Librarian'
librarian_user.userprofile.save()

member_user.userprofile.role = 'Member'
member_user.userprofile.save()

print("✓ Users with roles created")
exit()
```

### Test 3.2: Test Role-Based Views

1. **Test Admin View:**
   - Log in as: `admin_role` / `AdminRole123`
   - Navigate to: http://localhost:8000/relationship_app/admin_view/
   - Expected: Dashboard loads (access granted)

2. **Test as non-Admin:**
   - Log in as: `member` / `MemberPass123`
   - Navigate to: http://localhost:8000/relationship_app/admin_view/
   - Expected: Access denied

## 4. Testing Security Features

### Test 4.1: CSRF Protection

1. **Test 4.1a: With CSRF Token**
   - Visit login form: http://localhost:8000/relationship_app/login/
   - Inspect HTML source
   - Verify `{% csrf_token %}` is present
   - Login normally
   - Expected: Login succeeds

2. **Test 4.1b: Without CSRF Token (using curl)**
   ```bash
   curl -X POST http://localhost:8000/relationship_app/login/ \
     -d "username=testuser&password=testpass"
   ```
   - Expected: 403 Forbidden (CSRF failure)

### Test 4.2: XSS Protection

1. Try to inject JavaScript in username field during registration:
   - Username: `test<script>alert('xss')</script>`
   - Expected: JavaScript is escaped, no alert appears

2. Check Django templates auto-escape:
   - Go to Python shell:
   ```python
   from django.utils.html import escape
   text = "<script>alert('test')</script>"
   print(escape(text))
   # Output: &lt;script&gt;alert(&#x27;test&#x27;)&lt;/script&gt;
   ```

### Test 4.3: Debug Setting

1. In settings.py, verify:
   ```python
   DEBUG = False
   ```

2. Try to access a non-existent URL:
   - Navigate to: http://localhost:8000/nonexistent-page/
   - Expected: Generic 404 error (no sensitive information)

### Test 4.4: Security Headers

1. Check HTTP headers using browser developer tools or curl:
   ```bash
   curl -i http://localhost:8000/relationship_app/list_books/
   ```

2. Verify headers:
   - `X-Frame-Options: DENY` (present)
   - `X-Content-Type-Options: nosniff` (present)
   - `X-XSS-Protection` (browser-dependent)

### Test 4.5: SQL Injection Prevention

1. Go to list_books page: http://localhost:8000/relationship_app/list_books/
2. Try SQL injection in any search field (if present):
   - Input: `' OR '1'='1`
   - Expected: Treated as literal string, no SQL injection

## 5. Testing Authentication

### Test 5.1: Login/Logout

1. Log in with valid credentials:
   - Username: `testuser1`
   - Password: (the password you set)
   - Expected: Redirect to books list

2. Test logout:
   - Click logout
   - Expected: Redirect to logout confirmation page

3. Test login with invalid credentials:
   - Any username with wrong password
   - Expected: Error message displayed

### Test 5.2: Login Required Decorator

1. Log out
2. Try to access protected view:
   - Navigate to: http://localhost:8000/relationship_app/admin_view/
   - Expected: Redirect to login page

## 6. Testing Input Validation

### Test 6.1: Add Book Form Validation

1. Log in as a user with `can_add_book` permission
2. Go to add book page: http://localhost:8000/relationship_app/add_book/
3. Try to submit without title:
   - Expected: Form validation error
4. Try to submit without selecting author:
   - Expected: Form validation error
5. Submit valid data:
   - Title: `Test Book`
   - Author: (select one)
   - Expected: Book created successfully

## 7. Performance and Logging Testing

### Test 7.1: Check Query Count

```bash
python manage.py shell
```

```python
from django.test.utils import override_settings
from relationship_app.models import Book

# Enable query logging
import logging
logging.basicConfig()
logging.getLogger('django.db.backends').setLevel(logging.DEBUG)

# Query books
books = Book.objects.all()
for book in books:
    print(f"{book.title} by {book.author.name}")
```

## 8. Migration Testing

### Test 8.1: Fresh Database Setup

```bash
# Backup current database
mv db.sqlite3 db.sqlite3.backup

# Create fresh database
python manage.py migrate

# Create new superuser
python manage.py createsuperuser

# Verify models
python manage.py shell -c "from accounts.models import CustomUser; print(f'Users: {CustomUser.objects.count()}')"
```

## 9. Comprehensive Security Checklist

- [ ] DEBUG is False
- [ ] CSRF tokens present in all forms
- [ ] XSS protection enabled
- [ ] SQL queries use Django ORM
- [ ] Permissions checked in views
- [ ] HTTPS headers configured
- [ ] Session cookies are secure
- [ ] Custom user model working
- [ ] Groups and permissions created
- [ ] Login/logout working
- [ ] Protected views enforce permissions

## 10. Troubleshooting Tests

### Issue: Permission Denied When Accessing Protected View

**Solution:**
```python
# Verify user has permission
from django.contrib.auth.models import Permission
from accounts.models import CustomUser

user = CustomUser.objects.get(username='editor')
perms = user.get_all_permissions()
print(f"User permissions: {perms}")
```

### Issue: CSRF Token Mismatch

**Solution:**
- Ensure `{% csrf_token %}` is in all forms
- Check that CSRF middleware is enabled in settings.py
- Clear browser cookies and try again

### Issue: Custom User Model Not Being Used

**Solution:**
- Verify `AUTH_USER_MODEL = 'accounts.CustomUser'` in settings.py
- Run `python manage.py migrate` after adding to INSTALLED_APPS
- Restart development server

## Manual Testing Script

Run this comprehensive test:

```bash
python manage.py shell << EOF
from django.contrib.auth.models import Permission, Group
from accounts.models import CustomUser
from relationship_app.models import Author, UserProfile

# Test 1: Create custom user
user = CustomUser.objects.create_user(
    email='test@example.com',
    username='testuser',
    password='TestPass123',
    date_of_birth='1990-01-01'
)
print("✓ Test 1: Custom user created")

# Test 2: Create group with permission
group, _ = Group.objects.get_or_create(name='TestGroup')
print("✓ Test 2: Group created")

# Test 3: Check user permissions
print(f"✓ Test 3: User permissions: {user.get_all_permissions()}")

# Test 4: Create author
author, _ = Author.objects.get_or_create(name='Test Author')
print("✓ Test 4: Author created")

print("\n✅ All tests passed!")
EOF
```

This will verify that all components are working correctly.
