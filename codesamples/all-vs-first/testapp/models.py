from django.db import models

class Edition(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    library = models.ForeignKey('Library', on_delete=models.CASCADE, related_name='books')
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Library(models.Model):
    name = models.CharField(max_length=100)

    @property
    def first_book_edition_name(self):
        # Note: using all() instead of first() to avoid an extra database query
        books = self.books.all()
        for book in books:
            return book.edition.name
        return None
    
    