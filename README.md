# DiveHQ/backend-internship-task

DiveHQ backend-internship-task
## Features

- User Registration: Users can create an account.
- User Login: Users can log in to their accounts.
- Role-based Authentication: Three roles with different permission levels - regular user, user manager, admin.
- CRUD Operations: Users can create, read, update, and delete their owned records.
- User Manager: User managers can CRUD users.
- Admin: Admins can CRUD all records and users.
- Entry Information: Each entry has a date, time, text, and number of calories.
- Calories API Integration: If calories are not provided, the API connects to a Calories API provider to fetch the number of calories for the entered meal.
- User Setting: Users can set their expected number of calories per day.
- Calorie Comparison: Each entry has a boolean field indicating if the total calories for the day are less than the expected number of calories.
- JSON API: Data is returned in JSON format.
- Filtering and Pagination: Endpoints provide filter capabilities and support pagination.
- Unit and E2E Tests: Includes unit tests and end-to-end tests.
- Python Web Framework: Uses any Python web framework.
- SQLite Database: Uses SQLite as the database.

## Installation and Setup

1. Clone the repository.

```shell
    git clone https://github.com/dxphilo/octo.git
``

Install the required dependencies.

```shell
    pip install -r requirements.txt
```
Set up the database.

```shell
    python manage.py migrate
```

Run the application.

```shell
    python manage.py runserver
```

Usage

Open the API documentation in your browser by visiting http://localhost:8000/docs.

Register a new user account.

Log in with the registered user account.

Explore the available endpoints and their functionality based on your role.

Testing

Run unit tests.

```shell
    python manage.py test
```

```shell
    python manage.py e2e_test
```

Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please create an issue or submit a pull request.

License

This project is licensed under the MIT License.

Please note that you should replace "Description of your project" with an actual description of your project. Additionally, ensure that you have an appropriate license file (e.g., `LICENSE`) in your project directory to correspond with the license mentioned in the README.md.