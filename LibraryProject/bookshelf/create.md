````markdown
Create a Book instance

Open the Django shell:

```bash
python manage.py shell
```

In the shell, run:

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
# Expected output: 1984 by George Orwell (1949)
```

This creates and saves a new `Book` record to the database. Make sure `bookshelf` is added to `INSTALLED_APPS` and migrations have been run before creating instances.

You can also run it non-interactively:

```bash
python manage.py shell -c "from bookshelf.models import Book; Book.objects.create(title='1984', author='George Orwell', publication_year=1949)"
```
````
