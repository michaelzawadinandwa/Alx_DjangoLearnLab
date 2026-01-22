import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.query_samples import query_books_by_author, query_books_in_library, query_librarian_for_library
from relationship_app.models import Author, Book, Library, Librarian

print("✓ All query functions imported successfully")

# Create test data
author = Author.objects.first() or Author.objects.create(name="Test Author")
book = Book.objects.first() or Book.objects.create(title="Test Book", author=author)
library = Library.objects.first() or Library.objects.create(name="Test Library")
library.books.add(book)
librarian = Librarian.objects.first() or Librarian.objects.create(name="Test Librarian", library=library)

# Test queries
print("\nTesting query_books_by_author...")
result = query_books_by_author(author.id)
print(f"✓ Found {result.count()} books by author")

print("\nTesting query_books_in_library...")
result = query_books_in_library(library.id)
print(f"✓ Found {result.count()} books in library")

print("\nTesting query_librarian_for_library...")
result = query_librarian_for_library(library.id)
print(f"✓ Found librarian: {result.name}")

print("\n✓ All queries working correctly!")
