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
```

Install the required dependencies.

```shell
    pip install -r requirements.txt
```
Set up the database.

```shell
    python create_db.py
```

Run the application.

```shell
    uvicorn main:app --reload
```

ENV Setup

Create a file named .env in the root directory of your project.
1. Open the .env file in a text editor.

2. Add the following lines to the .env file:

```shell
    PORT="8000"
    NUTRITIONIX_API_ID="your-api-id here"
    NUTRITIONIX_API_KEY="your-api-key-here"
    NUTRITIONIX_URL="https://trackapi.nutritionix.com/v2/search/item?nix_item_id=513fc9e73fe3ffd40300109f"
    EXPECTED_CALORIES_PER_DAY= 2000 // change this to your expected calories per day
```
Replace your_api_id and your_api_key with the actual values obtained from [https://www.nutritionix.com/](https://www.nutritionix.com/).

Make sure to save the .env file in the same directory as your Python files.



Usage

Open the API documentation in your browser by visiting http://localhost:8000/docs.

Register a new user account.

Log in with the registered user account.

Explore the available endpoints and their functionality based on your role.

Testing

Run unit tests.

```shell
    pytest
```

Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please create an issue or submit a pull request.

License

This project is licensed under the MIT License.

Please note that you should replace "Description of your project" with an actual description of your project. Additionally, ensure that you have an appropriate license file (e.g., `LICENSE`) in your project directory to correspond with the license mentioned in the README.md.