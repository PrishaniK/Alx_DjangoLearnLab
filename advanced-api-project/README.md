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
