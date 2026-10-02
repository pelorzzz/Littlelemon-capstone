# Little Lemon Capstone — Table Booking & Menu API

A Django + Django REST Framework project for the Little Lemon restaurant,
built for the back-end development capstone. Supports:

- Static HTML homepage served by Django
- Menu item API (list/create/update/delete, Manager-only writes)
- Table booking API (authenticated users only, scoped to their own bookings)
- User registration & token-based login
- Unit tests for models and API views
- MySQL-ready settings (SQLite by default for zero-setup local dev)

## 1. Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the homepage, or `http://127.0.0.1:8000/admin/`
for the Django admin.

## 2. Switching to MySQL

1. `pip install mysqlclient` (also add it to `requirements.txt` — the line is
   already there, just uncomment it).
2. Create the database: `CREATE DATABASE littlelemon_db;`
3. In `littlelemon/settings.py`, replace the `DATABASES` dict with the
   MySQL block that's commented out directly below it, and set the
   `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` environment
   variables (or hardcode them for local dev only — never commit real
   credentials).
4. Re-run `python manage.py migrate`.

## 3. Running the tests

```bash
python manage.py test
```

## 4. Making a user a Manager

Only users in the `Manager` group can create, update, or delete menu items.
Everyone else (once authenticated) can only read the menu.

```bash
python manage.py shell
>>> from django.contrib.auth.models import User, Group
>>> group, _ = Group.objects.get_or_create(name='Manager')
>>> User.objects.get(username='your_username').groups.add(group)
```

## 5. API reference

| Method | Endpoint                  | Auth required | Notes                          |
|--------|----------------------------|----------------|---------------------------------|
| GET    | `/api/menu-items/`         | Yes            | List all menu items             |
| POST   | `/api/menu-items/`         | Manager only   | Create a menu item              |
| GET    | `/api/menu-items/<id>/`    | Yes            | Retrieve one item                |
| PUT    | `/api/menu-items/<id>/`    | Manager only   | Update an item                  |
| DELETE | `/api/menu-items/<id>/`    | Manager only   | Delete an item                  |
| GET    | `/api/bookings/`           | Yes            | List the logged-in user's bookings |
| POST   | `/api/bookings/`           | Yes            | Create a booking                |
| GET/PUT/DELETE | `/api/bookings/<id>/` | Yes          | Manage one booking (owner only) |
| POST   | `/api/registration/`       | No             | Create a user, returns a token  |
| POST   | `/api/login/`              | No             | Returns a token for a user      |

Authenticate requests by adding the header:
`Authorization: Token <token-from-registration-or-login>`

## 6. Git workflow for submission

```bash
git init
git add .
git commit -m "Little Lemon capstone: booking + menu API, auth, tests"
git branch -M main
git remote add origin <your-empty-github-repo-url>
git push -u origin main
```

Make sure `Readme.txt` (listing the API paths for your peer reviewers) is
committed and pushed along with the rest of the code.
