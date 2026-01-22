````markdown

Update the `Book` title and save the change

Open the Django shell:

```bash
python manage.py shell
```

In the shell, run:

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)  # Expected output: Nineteen Eighty-Four
print(book)        # Expected output: Nineteen Eighty-Four by George Orwell (1949)
```

Non-interactive one-liner:

```bash
python manage.py shell -c "from bookshelf.models import Book; b=Book.objects.get(title='1984'); b.title='Nineteen Eighty-Four'; b.save(); print(b.title)"
```

Ensure `bookshelf` is in `INSTALLED_APPS` and migrations have been applied before running these commands.


````
