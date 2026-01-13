```markdown
CRUD operations performed via Django shell

1) Create

```py
from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(b)
# Expected: <Book: 1984 by George Orwell (1949)>
```

2) Retrieve

```py
from bookshelf.models import Book
book = Book.objects.get(id=b.id)
print(book.title)            # Expected: 1984
print(book.author)           # Expected: George Orwell
print(book.publication_year) # Expected: 1949
print(list(Book.objects.all()))
# Expected: [<Book: 1984 by George Orwell (1949)>]
```

3) Update

```py
book.title = "Nineteen Eighty-Four"
book.save()
print(Book.objects.get(id=book.id))
# Expected: <Book: Nineteen Eighty-Four by George Orwell (1949)>
```

4) Delete

```py
book.delete()
print(list(Book.objects.all()))
# Expected: []
```

Ensure `bookshelf` is in `INSTALLED_APPS` and migrations have been applied before running these commands.
```
