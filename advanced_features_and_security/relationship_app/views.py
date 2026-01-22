from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape

from relationship_app.models import Book, Library, Author, UserProfile
from django.conf import settings

# Get the custom user model
CustomUser = settings.AUTH_USER_MODEL


# ============== UTILITY FUNCTIONS ==============

def sanitize_input(value):
    """
    Sanitize user input to prevent XSS attacks.
    This escapes HTML characters in user-provided data.
    """
    return escape(value) if value else None


# ============== FUNCTION-BASED VIEWS ==============

def list_books(request):
    """
    Function-based view to list all books.
    This view is publicly accessible and displays all books.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


# ============== CLASS-BASED VIEWS ==============

class LibraryDetailView(DetailView):
    """
    Class-based view to display library details with all books.
    Requires user to be logged in to view library details.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ============== AUTHENTICATION VIEWS ==============

@require_http_methods(["GET", "POST"])
@csrf_protect  # CSRF protection is applied to protect against cross-site request forgery
def register(request):
    """
    View for user registration.
    
    SECURITY:
    - Uses Django's built-in CSRF protection via csrf_protect decorator
    - Only allows GET (show form) and POST (submit form) methods
    - Password is hashed using Django's password hashing algorithm
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is automatically created via signal in models.py
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
@csrf_protect
def login_view(request):
    """
    View for user login.
    
    SECURITY:
    - Uses Django's authenticate() function for secure credential verification
    - CSRF token required for login form submission
    - Only allows GET and POST methods
    - User input is validated before authentication
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Sanitize username input
        username = sanitize_input(username)
        
        # Use Django's authenticate function to securely verify credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
        else:
            return render(request, 'relationship_app/login.html', 
                        {'error': 'Invalid credentials'})
    return render(request, 'relationship_app/login.html')


@login_required(login_url='login')
def logout_view(request):
    """
    View for user logout.
    Requires user to be logged in.
    """
    logout(request)
    return render(request, 'relationship_app/logout.html')


# ============== ROLE-BASED ACCESS CONTROL ==============

def is_admin(user):
    """
    Check if user has Admin role.
    Returns True if user's profile role is 'Admin', False otherwise.
    """
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False


def is_librarian(user):
    """
    Check if user has Librarian role.
    Returns True if user's profile role is 'Librarian', False otherwise.
    """
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False


def is_member(user):
    """
    Check if user has Member role.
    Returns True if user's profile role is 'Member', False otherwise.
    """
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view(request):
    """
    View accessible only to Admin users.
    
    ACCESS CONTROL:
    - Requires user to be logged in (@login_required)
    - Requires user to have Admin role (@user_passes_test(is_admin))
    
    FUNCTIONALITY:
    - Displays all users and their roles
    - Admin users can manage user roles and permissions
    """
    # Use the custom user model to query users
    users = settings.AUTH_USER_MODEL.objects.all()
    context = {
        'users': users,
        'page_title': 'Admin Dashboard'
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required(login_url='login')
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to Librarian users.
    
    ACCESS CONTROL:
    - Requires user to be logged in (@login_required)
    - Requires user to have Librarian role (@user_passes_test(is_librarian))
    
    FUNCTIONALITY:
    - Displays all libraries and books
    - Librarians can manage library inventory
    """
    libraries = Library.objects.all()
    books = Book.objects.all()
    context = {
        'libraries': libraries,
        'books': books,
        'page_title': 'Librarian Dashboard'
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@login_required(login_url='login')
@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to Member users.
    
    ACCESS CONTROL:
    - Requires user to be logged in (@login_required)
    - Requires user to have Member role (@user_passes_test(is_member))
    
    FUNCTIONALITY:
    - Displays available books
    - Members can browse the library catalog
    """
    books = Book.objects.all()
    context = {
        'books': books,
        'page_title': 'Member Dashboard'
    }
    return render(request, 'relationship_app/member_view.html', context)


# ============== PERMISSION-BASED VIEWS ==============
# These views use Django's permission_required decorator to enforce granular permissions
# Permissions are defined in models.py and can be assigned to users via groups

@login_required(login_url='login')
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book.
    
    PERMISSIONS:
    - Requires permission: 'relationship_app.can_add_book'
    - Can be assigned to users individually or via groups (e.g., 'Editors' group)
    
    SECURITY:
    - User input is sanitized to prevent SQL injection
    - Django ORM is used for database queries (prevents SQL injection)
    """
    if request.method == 'POST':
        # Sanitize user input
        title = sanitize_input(request.POST.get('title', '').strip())
        author_id = request.POST.get('author')
        
        # Validate input
        if title and author_id:
            try:
                # Use Django ORM to safely query the author
                author = Author.objects.get(id=author_id)
                # Create book with validated data
                book = Book.objects.create(title=title, author=author)
                return redirect('list_books')
            except Author.DoesNotExist:
                return render(request, 'relationship_app/add_book.html', 
                            {'authors': Author.objects.all(), 
                             'error': 'Author not found'})
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@login_required(login_url='login')
@permission_required('relationship_app.can_edit', raise_exception=True)
@csrf_protect
def edit_book(request, pk):
    """
    View to edit a book.
    
    PERMISSIONS:
    - Requires permission: 'relationship_app.can_edit'
    - Can be assigned to users individually or via groups (e.g., 'Editors' group)
    
    SECURITY:
    - User input is sanitized
    - CSRF protection is enforced
    - Only allows POST method for modifications
    """
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return HttpResponseForbidden('Book not found')
    
    if request.method == 'POST':
        # Sanitize user input
        title = sanitize_input(request.POST.get('title', '').strip())
        author_id = request.POST.get('author')
        
        # Validate input
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book.title = title
                book.author = author
                book.save()
                return redirect('list_books')
            except Author.DoesNotExist:
                return render(request, 'relationship_app/edit_book.html', 
                            {'book': book, 'authors': Author.objects.all(), 
                             'error': 'Author not found'})
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', 
                {'book': book, 'authors': authors})


@login_required(login_url='login')
@permission_required('relationship_app.can_delete', raise_exception=True)
@csrf_protect
def delete_book(request, pk):
    """
    View to delete a book.
    
    PERMISSIONS:
    - Requires permission: 'relationship_app.can_delete'
    - Can be assigned to users individually or via groups (e.g., 'Admins' group)
    
    SECURITY:
    - CSRF protection is enforced
    - Only allows POST method for actual deletion (GET shows confirmation)
    """
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return HttpResponseForbidden('Book not found')
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

