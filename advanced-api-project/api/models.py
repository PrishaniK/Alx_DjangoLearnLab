from django.db import models

class Author(models.Model):
    """One author; reverse access to books via author.books."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """A book linked to exactly one author (one-to-many)."""
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

