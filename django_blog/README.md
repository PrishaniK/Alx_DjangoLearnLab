### Authentication
- Register: `/register/` (username, email, password)
- Login: `/login/`
- Logout: `/logout/`
- Profile: `/profile/` (edit first/last name, email)

Built with:
- Django auth views for login/logout
- Custom `RegistrationForm` (extends `UserCreationForm`)
- `ProfileForm` (edits User fields)
- CSRF protection in all forms
