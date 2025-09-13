## Permissions and Groups Setup

### Custom Permissions
The `Book` model defines the following custom permissions:
- `can_view` - View books
- `can_create` - Add new books
- `can_edit` - Edit existing books
- `can_delete` - Delete books

### Groups
The following groups are created using the `setup_groups` management command:
- **Viewers**: Has `can_view`
- **Editors**: Has `can_view`, `can_create`, `can_edit`
- **Admins**: Has all permissions

### How to Apply
Run:
```bash
python manage.py setup_groups
