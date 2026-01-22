````markdown

Retrieve the `Book` instance and display its attributes

Open the Django shell:

```bash
python manage.py shell
```

In the shell, run:

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title)            # Expected output: 1984
print(book.author)           # Expected output: George Orwell
print(book.publication_year) # Expected output: 1949

# Or show a dictionary-like representation:
print(Book.objects.filter(title="1984").values())
# Expected output: [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]
```

Non-interactive one-liner:

```bash
python manage.py shell -c "from bookshelf.models import Book; print(list(Book.objects.filter(title='1984').values()))"
```

Ensure `bookshelf` is in `INSTALLED_APPS` and migrations have been applied before running these commands.


````
