## Generic Views for Books

Endpoints (all under `/api/gv/books/`):
- `GET /` — List all books (AllowAny) → `BookListGV (ListAPIView)`
- `GET /<pk>/` — Retrieve one (AllowAny) → `BookDetailGV (RetrieveAPIView)`
- `POST /create/` — Create (IsAuthenticated) → `BookCreateGV (CreateAPIView)`
- `PUT/PATCH /<pk>/update/` — Update (IsAuthenticated) → `BookUpdateGV (UpdateAPIView)`
- `DELETE /<pk>/delete/` — Delete (IsAuthenticated) → `BookDeleteGV (DestroyAPIView)`

### Customizations
- `perform_create/perform_update` trim the `title` before saving.
- Validation rule: `publication_year` cannot be in the future (in `BookSerializer`).

### Permissions
- Read-only endpoints: public (AllowAny).
- Write endpoints: authenticated users only (IsAuthenticated).
  - Quick test: `python manage.py createsuperuser`, log into `/admin/`, then use the browsable API.

### Notes
- ViewSets remain available at `/api/books/` and `/api/authors/`.
- Nested `books` on authors are read-only via `AuthorSerializer(books=BookSerializer(many=True, read_only=True))`.


### Filtering, Searching, Ordering (Books)
- Filter: `/api/books/?title=Coraline&publication_year=2002&author=1&author__name=Neil`
- Search (icontains): `/api/books/?search=neil`
- Ordering: `/api/books/?ordering=title` or `/api/books/?ordering=-publication_year`

Enabled via:
- `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`
- `filterset_fields = ["title", "publication_year", "author", "author__name"]`
- `search_fields = ["title", "author__name"]`
- `ordering_fields = ["title", "publication_year", "id"]`
