from django.db import models
import uuid


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Book(models.Model):
    id_store = models.UUIDField(default=uuid.uuid4, primary_key=True,
                                help_text="The unique identifier for this particular book in the warehouse and shop")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class BookItem(models.Model):
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookitem')
    row = models.IntegerField()
    shelf = models.CharField(max_length=5)
    history = models.BooleanField()

    def __str__(self):
        return self.isbn