"""Sample query utilities for `relationship_app`.

Run this script after you have added the app to INSTALLED_APPS, run
`python manage.py makemigrations relationship_app` and `python manage.py migrate`.

It configures Django, imports the models and demonstrates three queries:
- Query all books by a specific author
- List all books in a library
- Retrieve the librarian for a library

This file is intended to be executed directly from the project root or by
running `python relationship_app/query_samples.py` from the project root.
"""

import os
import sys
from typing import List


def setup_django():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
    import django
    django.setup()


def get_books_by_author(author_name: str) -> List[str]:
    from relationship_app.models import Book
    qs = Book.objects.filter(author__name=author_name)
    return [b.title for b in qs]


def list_books_in_library(library_name: str) -> List[str]:
    from relationship_app.models import Library
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return [b.title for b in library.books.all()]


def get_librarian_for_library(library_name: str) -> str:
    from relationship_app.models import Library
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return ""
    # Access the OneToOne relation via the related_name `librarian`
    if hasattr(library, 'librarian') and library.librarian is not None:
        return library.librarian.name
    return ""


if __name__ == "__main__":
    setup_django()
    print("Sample queries — ensure migrations have been applied and data exists.")

    author = "Example Author"
    print(f"Books by '{author}':")
    for t in get_books_by_author(author):
        print(" -", t)

    library = "Main Library"
    print(f"\nBooks in library '{library}':")
    for t in list_books_in_library(library):
        print(" -", t)

    print(f"\nLibrarian for library '{library}':")
    lib_name = get_librarian_for_library(library)
    print(" -", lib_name if lib_name else "(none)")
