from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Full serializer for /api/books/ (includes 'author')."""
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Author with nested books for read/write.
    We accept books WITHOUT 'author' and set author=instance in code.
    """
    books = BookSerializer(many=True, required=False)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]

    def create(self, validated_data):
        books_data = validated_data.pop("books", [])
        author = Author.objects.create(**validated_data)
        # Reuse BookSerializer to enforce the future-year validation
        for b in books_data:
            bs = BookSerializer(data={**b, "author": author.id})
            bs.is_valid(raise_exception=True)
            bs.save()
        return author

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if "books" in validated_data:
            instance.books.all().delete()
            for b in validated_data["books"]:
                bs = BookSerializer(data={**b, "author": instance.id})
                bs.is_valid(raise_exception=True)
                bs.save()
        return instance

