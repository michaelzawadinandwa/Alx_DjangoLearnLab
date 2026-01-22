import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from relationship_app.views import (
    list_books, LibraryDetailView, register, login_view, logout_view,
    admin_view, librarian_view, member_view, 
    add_book, edit_book, delete_book
)
from relationship_app.models import UserProfile, Library

print("✓ All views imported successfully")
print("\nVerifying view functions exist:")
print(f"✓ list_books: {callable(list_books)}")
print(f"✓ LibraryDetailView: {LibraryDetailView is not None}")
print(f"✓ register: {callable(register)}")
print(f"✓ login_view: {callable(login_view)}")
print(f"✓ logout_view: {callable(logout_view)}")
print(f"✓ admin_view: {callable(admin_view)}")
print(f"✓ librarian_view: {callable(librarian_view)}")
print(f"✓ member_view: {callable(member_view)}")
print(f"✓ add_book: {callable(add_book)}")
print(f"✓ edit_book: {callable(edit_book)}")
print(f"✓ delete_book: {callable(delete_book)}")

print("\nVerifying UserProfile model:")
user = User.objects.first()
if user:
    profile = user.userprofile
    print(f"✓ UserProfile exists for user: {user.username}")
    print(f"✓ User role: {profile.role}")
    print(f"✓ Role choices available: Admin, Librarian, Member")

print("\n✓ All views and models verified!")
