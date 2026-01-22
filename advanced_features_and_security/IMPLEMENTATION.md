# Django Models - Advanced Relationships and Authentication

This project demonstrates advanced Django ORM capabilities including complex model relationships, user authentication, role-based access control, and custom permissions.

## Project Structure

```
django-models/
├── db.sqlite3
├── manage.py
├── README.md
├── bookshelf/                          # Basic Django app
├── LibraryProject/                     # Main project settings
├── relationship_app/                   # Advanced features app
│   ├── migrations/
│   ├── templates/relationship_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── query_samples.py
```

## Features Implemented

### 1. Advanced Model Relationships

#### Models Created:
- **Author**: Basic model with name field
- **Book**: Has ForeignKey relationship to Author
- **Library**: Has ManyToMany relationship to Book
- **Librarian**: Has OneToOne relationship to Library
- **UserProfile**: Extended User model with role-based choices

#### Relationships:
- **ForeignKey**: Book → Author (one book has one author, one author can have many books)
- **ManyToMany**: Library ↔ Book (one library has many books, one book can be in many libraries)
- **OneToOne**: Librarian → Library (one librarian manages one library, one library has one librarian)

### 2. Views Implementation

#### Function-based Views:
- `list_books()`: Displays all books in the database

#### Class-based Views:
- `LibraryDetailView`: DetailView showing library information and its books

#### Authentication Views:
- `register()`: User registration with UserCreationForm
- `login_view()`: User login functionality
- `logout_view()`: User logout functionality

#### Role-Based Access Control Views:
- `admin_view()`: Restricted to Admin role users (displays all users and their roles)
- `librarian_view()`: Restricted to Librarian role users (displays libraries and books)
- `member_view()`: Restricted to Member role users (displays available books)

#### Permission-Based Views:
- `add_book()`: Requires `can_add_book` permission
- `edit_book()`: Requires `can_change_book` permission
- `delete_book()`: Requires `can_delete_book` permission

### 3. User Authentication System

- User registration with automatic UserProfile creation via Django signals
- User login and logout functionality
- Session management
- Login required decorators on protected views

### 4. Role-Based Access Control (RBAC)

#### UserProfile Model:
```python
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
```

#### Automatic Profile Creation:
Django signals automatically create a UserProfile when a new user is registered.

#### Role Checking:
```python
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view(request):
    # Only Admin users can access
    pass
```

### 5. Custom Permissions

#### Book Model Permissions:
```python
class Meta:
    permissions = [
        ('can_add_book', 'Can add a book'),
        ('can_change_book', 'Can change a book'),
        ('can_delete_book', 'Can delete a book'),
    ]
```

#### Permission Enforcement:
```python
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # Only users with can_add_book permission can access
    pass
```

## URL Configuration

All URLs are prefixed with the base path and routed as follows:

| URL | View | Method | Description |
|-----|------|--------|-------------|
| `/books/` | list_books | GET | List all books |
| `/library/<id>/` | LibraryDetailView | GET | Show library details |
| `/login/` | login_view | GET, POST | User login |
| `/logout/` | logout_view | GET, POST | User logout |
| `/register/` | register | GET, POST | User registration |
| `/admin/` | admin_view | GET | Admin dashboard (Admin only) |
| `/librarian/` | librarian_view | GET | Librarian dashboard (Librarian only) |
| `/member/` | member_view | GET | Member dashboard (Member only) |
| `/add-book/` | add_book | GET, POST | Add new book (requires permission) |
| `/edit-book/<id>/` | edit_book | GET, POST | Edit book (requires permission) |
| `/delete-book/<id>/` | delete_book | GET, POST | Delete book (requires permission) |

## Templates

### Authentication Templates:
- `login.html`: Login form
- `register.html`: User registration form
- `logout.html`: Logout confirmation page

### Content Templates:
- `list_books.html`: Display all books
- `library_detail.html`: Display library details with books
- `add_book.html`: Form to add a new book
- `edit_book.html`: Form to edit a book
- `delete_book.html`: Confirmation page to delete a book

### Role-Based Templates:
- `admin_view.html`: Admin dashboard
- `librarian_view.html`: Librarian dashboard
- `member_view.html`: Member dashboard

## Query Examples (from query_samples.py)

### Query 1: Get all books by a specific author
```python
def query_books_by_author(author_id):
    author = Author.objects.get(id=author_id)
    books = author.books.all()
    return books
```

### Query 2: Get all books in a library
```python
def query_books_in_library(library_id):
    library = Library.objects.get(id=library_id)
    books = library.books.all()
    return books
```

### Query 3: Get the librarian for a library
```python
def query_librarian_for_library(library_id):
    library = Library.objects.get(id=library_id)
    librarian = library.librarian
    return librarian
```

## Usage Instructions

### 1. Create Sample Data

```bash
# Create a superuser for admin access
python manage.py createsuperuser

# Access Django admin at http://localhost:8000/admin/
```

### 2. Create Test Users with Different Roles

You can assign roles to users through Django admin:
1. Go to Admin panel
2. Create or select users
3. Edit their UserProfile to assign roles (Admin, Librarian, Member)

### 3. Run the Development Server

```bash
python manage.py runserver
```

### 4. Access the Application

- Homepage: `http://localhost:8000/books/`
- Admin Dashboard: `http://localhost:8000/admin/`
- Login: `http://localhost:8000/login/`
- Register: `http://localhost:8000/register/`

## Security Features

1. **CSRF Protection**: All forms include `{% csrf_token %}`
2. **Password Hashing**: Django's built-in user authentication
3. **Login Required**: Sensitive views require authentication
4. **Role-Based Access**: Views check user roles before allowing access
5. **Permission Checking**: Custom permissions control resource modification
6. **Exception Handling**: Permission denied responses for unauthorized access

## Database Migrations

```bash
# Create migrations
python manage.py makemigrations relationship_app

# Apply migrations
python manage.py migrate
```

## Admin Interface

The admin interface includes:
- Author management
- Book management with filtering by author
- Library management
- Librarian management
- UserProfile management with role filtering

## Testing the Application

1. **Register a new user**: Go to `/register/` and create an account
2. **Login**: Navigate to `/login/` with your credentials
3. **View books**: Access `/books/` to see all books
4. **View libraries**: Click on a library from the list to see its details
5. **Role-based access**: Admin can access `/admin/`, Librarians can access `/librarian/`

## Requirements

- Django 6.0+
- Python 3.8+
- SQLite3 (included in Django)

## Future Enhancements

- Add publication year to Book model
- Implement search functionality
- Add pagination to book listings
- Create user profile page
- Add book ratings/reviews
- Implement book reservations system
- Add API endpoints with Django REST Framework
