# Test Challenge

Simple Django REST Framework app where users can register, verify their emails, create teams and invite others to join the app.
Users can reset their passwords and create their own teams.
Invites are sent via email.

The app uses `django-allauth` app under the hood.

### Local dev install

To run locally:

* you would need Python 3.6 within virtual environment installed the way you prefer;
* create new PostgreSQL database and user with all privileges and `CREATEDB`, i.e.:
```
CREATE DATABASE db_name;
CREATE USER user_name WITH PASSWORD 'user_password';
GRANT ALL PRIVILEGES ON DATABASE "db_name" to user_name;
ALTER USER user_name CREATEDB;
```
* clone the repo;
* within the virtual env - install requirements, migrate:
```
$ pip install -r requirements/local.txt
$ python manage.py migrate
$ python manage.py createsuperuser
```

### Tests

Run tests with pytest and coverage from the directory that contains `pytest.ini` file:
```
$ pytest
```
Coverage results are in `htmlcov/index.html`

### API

Users must be authenticated to access the API. Authentication is implemented with JWT tokens. To get a token, users should `POST` to `/auth/login/` with their `email` and `password`. 
After obtaining the token, it should be included into all the subsequent requests in the header `Authorization: JWT <token>` - use Postman or a similar tool. Logging out should be implemented on the front-end, i.e. by removing the JWT token.

* `/api/` - API root

    * `/teams/` 
        - `GET` - lists the teams. Creating teams can be done via `POST` `/users/<pk>/teams/`
    * `/teams/<pk>/`
        - `GET` - team details
        - `PUT`, `PATCH` - replaces, updates the existing team (expects `name` arg) - can be done only by a member of that team.
    * `/users/` 
        - `GET` - lists the users
    * `/users/<pk>/`
        - `GET` - user details
        - `PUT`, `PATCH` - replaces, updates the existing user - can be done only by the user him/herself or by the admin.
    * `/users/<pk>/invite/`
        - `POST` - send invitation, expects `email` of the invitee
    * `/users/<member_pk>/teams/`
        - `GET` - lists the team of user with `pk == member_pk`
        - `POST` - create new Team and become a member of it - available only if the user doesn't have a team yet (expects `name`)
        - `PUT`, `PATCH` - replace, update the team of user with `pk == member_pk`
* `/auth/` - manage accounts
    * `/login/`
        - `POST` - log the user in - expects `email`, `password`. Returns JWT token.
    * `/registration/`
        - `POST` - registers the user and creates the account, sends verification link via email - User can access the app once he/she verifies the email. Expects `email`, `password1`, `password2`. 
    * `/password/reset/`
        - `POST` - initiates the password reset mechanism (if the user forgot the password) - sends reset link via email. Expects `email` parameter.
    * `/password/change/`
        - `POST` - changes the password. Expects `old_password`, `new_password1` and `new_password2`

There are standard `django-allauth` urls included in the app as well to provide basic front-end for invitation signup, password reset forms and so on:
* `/accounts/login/`
* `/accounts/logout/`
* `/accounts/signup/`
