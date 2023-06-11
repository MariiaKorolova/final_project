from django.db import models
import uuid


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return self.first_name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("title", max_length=255)
    author = models.ManyToManyField(Author, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    id_in_store = models.UUIDField(default=uuid.uuid4, primary_key=True,
                                   help_text="The unique identifier for this particular book in the warehouse and shop")

    def __str__(self):
        return self.title