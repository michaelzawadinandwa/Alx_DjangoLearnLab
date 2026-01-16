````markdown

Delete the `Book` instance and confirm deletion

Open the Django shell:

```bash
python manage.py shell
```

In the shell, run:

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
# Delete the book
book.delete()

# Confirm deletion - no books should remain
print(list(Book.objects.all()))
# Expected output: []

# Or show values for clarity:
print(list(Book.objects.values()))
# Expected output: []
```

Non-interactive one-liner:

```bash
python manage.py shell -c "from bookshelf.models import Book; Book.objects.filter(title='Nineteen Eighty-Four').delete(); print(list(Book.objects.values()))"
```

Ensure `bookshelf` is in `INSTALLED_APPS` and migrations have been applied before running these commands.


````
