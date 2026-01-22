"""
Sample queries demonstrating Django ORM relationships
This script contains queries for ForeignKey, ManyToMany, and OneToOne relationships
"""

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_id):
    """
    Query all books by a specific author.
    
    Args:
        author_id: The ID of the author
        
    Returns:
        QuerySet of all books written by the author
    """
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author)
    # Alternative using related_name:
    # books = author.books.all()
    return books


def query_books_in_library(library_id):
    """
    List all books in a library.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        QuerySet of all books in the library
    """
    library = Library.objects.get(id=library_id)
    books = library.books.all()
    return books


def query_librarian_for_library(library_id):
    """
    Retrieve the librarian for a library.
    
    Args:
        library_id: The ID of the library
        
    Returns:
        The Librarian object associated with the library
    """
    library = Library.objects.get(id=library_id)
    librarian = library.librarian
    # Alternative using direct query:
    # librarian = Librarian.objects.get(library_id=library_id)
    return librarian


# Example usage and testing
if __name__ == '__main__':
    # Note: These examples assume sample data has been created
    
    # Example 1: Query books by a specific author
    print("=== Query Books by Author ===")
    try:
        author_books = query_books_by_author(1)
        for book in author_books:
            print(f"Book: {book.title}")
    except Author.DoesNotExist:
        print("Author not found")
    
    # Example 2: List all books in a library
    print("\n=== Books in Library ===")
    try:
        library_books = query_books_in_library(1)
        for book in library_books:
            print(f"Book: {book.title}")
    except Library.DoesNotExist:
        print("Library not found")
    
    # Example 3: Retrieve the librarian for a library
    print("\n=== Librarian for Library ===")
    try:
        librarian = query_librarian_for_library(1)
        print(f"Librarian: {librarian.name}")
    except Library.DoesNotExist:
        print("Library not found")
    except Librarian.DoesNotExist:
        print("Librarian not found for this library")
