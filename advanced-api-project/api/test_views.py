# api/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Author, Book

User = get_user_model()


class BookAPITests(TestCase):
    """
    Tests cover:
      - Read endpoints (public)
      - Create/Update/Delete (auth required on CBV endpoints)
      - Filtering, Searching, Ordering on list endpoints
      - Validation: publication_year not in the future
    Endpoints under project prefix /api/ as configured in advanced_api_project/urls.py
    """

    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # API clients
        self.anon = APIClient()
        self.auth = APIClient()
        self.auth.force_authenticate(user=self.user)

        # Data
        self.author1 = Author.objects.create(name="Neil Gaiman")
        self.author2 = Author.objects.create(name="Terry Pratchett")

        self.book1 = Book.objects.create(
            title="American Gods", publication_year=2001, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Coraline", publication_year=2002, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Good Omens", publication_year=1990, author=self.author2
        )

        # Common URLs (CBV ones are the ones with permissions)
        self.list_url = "/api/books/"               # ListView (CBV) mounted at path("books/", ...)
        self.create_url = "/api/books/create/"      # CreateView (IsAuthenticated)
        # Update/Delete take pk:
        self.update_url = lambda pk: f"/api/books/update/{pk}/"
        self.delete_url = lambda pk: f"/api/books/delete/{pk}/"

        # Router list also exists at /api/books/ via ViewSet; our CBV uses same path.
        # Both support filtering/search/ordering because we enabled them on both.

    # ---------- READ (public) ----------
    def test_public_list_ok(self):
        res = self.anon.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 3)

    def test_public_detail_ok(self):
        res = self.anon.get(f"/api/books/{self.book1.id}/")
        # RetrieveAPIView (CBV) is mounted at "books/<int:pk>/" — public read
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.book1.id)

    # ---------- CREATE (auth required) ----------
    def test_create_requires_auth(self):
        payload = {
            "title": "New Book",
            "publication_year": 2011,
            "author": self.author1.id,
        }
        res = self.anon.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_ok_when_authenticated(self):
        payload = {
            "title": "  Clean Coder  ",  # leading/trailing spaces will be trimmed by perform_create
            "publication_year": 2011,
            "author": self.author1.id,
        }
        res = self.auth.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Clean Coder")

    def test_create_rejects_future_year(self):
        payload = {
            "title": "Future Book",
            "publication_year": 3000,
            "author": self.author1.id,
        }
        res = self.auth.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    # ---------- UPDATE (auth required) ----------
    def test_update_requires_auth(self):
        payload = {"title": "American Gods (Updated)", "publication_year": 2001, "author": self.author1.id}
        res = self.anon.put(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_ok_when_authenticated(self):
        payload = {"title": "  American Gods (Updated)  ", "publication_year": 2001, "author": self.author1.id}
        res = self.auth.put(self.update_url(self.book1.id), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "American Gods (Updated)")

    # ---------- DELETE (auth required) ----------
    def test_delete_requires_auth(self):
        res = self.anon.delete(self.delete_url(self.book2.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_ok_when_authenticated(self):
        res = self.auth.delete(self.delete_url(self.book2.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm it is gone
        res2 = self.anon.get(f"/api/books/{self.book2.id}/")
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- FILTERING ----------
    def test_filter_by_publication_year(self):
        res = self.anon.get(f"{self.list_url}?publication_year=2002")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Coraline", titles)
        self.assertNotIn("American Gods", titles)

    def test_filter_by_author_id(self):
        res = self.anon.get(f"{self.list_url}?author={self.author2.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b["author"] == self.author2.id for b in res.data))

    def test_filter_by_author_name(self):
        res = self.anon.get(f"{self.list_url}?author__name=Neil Gaiman")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("American Gods", titles)
        self.assertIn("Coraline", titles)
        self.assertNotIn("Good Omens", titles)

    # ---------- SEARCH ----------
    def test_search_title_or_author(self):
        res = self.anon.get(f"{self.list_url}?search=coral")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Coraline", titles)

        res2 = self.anon.get(f"{self.list_url}?search=neil")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        titles2 = [b["title"] for b in res2.data]
        # Both Neil's books should appear
        self.assertIn("American Gods", titles2)
        self.assertIn("Coraline", titles2)

    # ---------- ORDERING ----------
    def test_ordering_by_publication_year_desc(self):
        res = self.anon.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))
