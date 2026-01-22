from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods

from relationship_app.models import Book, Library, Author, UserProfile


# ============== Function-based Views ==============

def list_books(request):
    """Function-based view to list all books"""
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


# ============== Class-based Views ==============

class LibraryDetailView(DetailView):
    """Class-based view to display library details with all books"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ============== Authentication Views ==============

@require_http_methods(["GET", "POST"])
def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is automatically created via signal
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """View for user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    """View for user logout"""
    logout(request)
    return render(request, 'relationship_app/logout.html')


# ============== Role-Based Access Control Views ==============

def is_admin(user):
    """Check if user has Admin role"""
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False


def is_librarian(user):
    """Check if user has Librarian role"""
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False


def is_member(user):
    """Check if user has Member role"""
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users"""
    # Admin can see all users and their roles
    users = User.objects.all()
    context = {
        'users': users,
        'page_title': 'Admin Dashboard'
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required(login_url='login')
@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users"""
    # Librarian can see all libraries and books
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
    """View accessible only to Member users"""
    # Members can see available books
    books = Book.objects.all()
    context = {
        'books': books,
        'page_title': 'Member Dashboard'
    }
    return render(request, 'relationship_app/member_view.html', context)


# ============== Permission-Based Views ==============

@login_required(login_url='login')
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book (requires can_add_book permission)"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book = Book.objects.create(title=title, author=author)
                return redirect('list_books')
            except Author.DoesNotExist:
                return render(request, 'relationship_app/add_book.html', 
                            {'authors': Author.objects.all(), 
                             'error': 'Author not found'})
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@login_required(login_url='login')
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit a book (requires can_change_book permission)"""
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return HttpResponseForbidden('Book not found')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
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
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book (requires can_delete_book permission)"""
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return HttpResponseForbidden('Book not found')
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})
