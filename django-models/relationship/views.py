from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from .models import Book, Library


# Task 1: Function-based View to list all books
def list_books(request):
    """Function-based view to list all books"""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Task 1: Class-based View to display library details
class LibraryDetailView(DetailView):
    """Class-based view to display library details"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Task 2: User Authentication Views
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


def user_logout(request):
    """User logout view"""
    logout(request)
    return render(request, 'relationship_app/logout.html')


# Task 3: Role-Based Access Control Views
def check_role(role):
    """Helper function to check user role"""
    def check(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role
    return check


@user_passes_test(check_role('Admin'))
def admin_view(request):
    """Admin-only view"""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    """Librarian-only view"""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(check_role('Member'))
def member_view(request):
    """Member-only view"""
    return render(request, 'relationship_app/member_view.html')


# Task 4: Views with Custom Permissions
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        # Handle book creation logic here
        messages.success(request, 'Book added successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """View to edit a book - requires can_change_book permission"""
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        # Handle book update logic here
        messages.success(request, 'Book updated successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book - requires can_delete_book permission"""
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})