# FastAPI Application
FastAPI
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

#### Clone the repository.

```shell
    git clone https://github.com/dxphilo/octo.git
```

#### ENV Setup

Create a file named .env in the root directory of your project.

```shell
    cp .env.example .env
```


#### Install the required dependencies.

```shell
    pip install -r requirements.txt
```
#### Set up the database with sqlite.

```shell
    python create_db.py
```

#### Run the application.

Application will be exposed to port 8000 on http://localhost:8000/

```shell
    python main.py
```

#### Testing

Running tests.

```shell
    pytest
```

### Usage

Open the API documentation in your browser by visiting http://localhost:8000/docs.


## API Endpoints

The following endpoints are available in the API:

Send token in the form: 

```ssh
  Authorization: Bearer <your-token-here>
```

### 1. Create a User

- **Endpoint**: `/signup/`
- **Method**: `POST`
- **Request Body**:
  - `fullname` (string): Full name of the user (required)
  - `email` (string): Email of the user (required)
  - `password` (string): Password of the user (required)
  - `role` (string): Role of the user (required)
- **Response**:
  - `id` (integer): ID of the created user
  - `fullname` (string): Full name of the created user
  - `email` (string): Email of the created user
  - `role` (string): Role of the created user
  - `date` (string): Current date
  - `time` (string): Current time

### 2. User Login

- **Endpoint**: `/login/`
- **Method**: `POST`
- **Request Body**:
  - `email` (string): Email of the user (required)
  - `password` (string): Password of the user (required)
- **Response**:
  - `access_token` (string): JWT access token for authentication

### 3. Get Users

- **Endpoint**: `/users/`
- **Method**: `GET`
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - List of user objects:
    - `id` (integer): ID of the user
    - `fullname` (string): Full name of the user
    - `email` (string): Email of the user
    - `role` (string): Role of the user
    - `date` (string): Current date
    - `time` (string): Current time

### 4. Update User Details

- **Endpoint**: `/users/{user_id}/`
- **Method**: `PUT`
- **Path Parameters**:
  - `user_id` (integer): ID of the user to update (required)
- **Request Body**:
  - `fullname` (string): New full name of the user (required)
  - `email` (string): New email of the user (required)
  - `password` (string): New password of the user (required)
  - `role` (string): New role of the user (required)
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `id` (integer): ID of the updated user
  - `fullname` (string): New full name of the user
  - `email` (string): New email of the user
  - `role` (string): New role of the user
  - `date` (string): Current date
  - `time` (string): Current time

### 5. Delete User

- **Endpoint**: `/users/{user_id}/`
- **Method**: `DELETE`
- **Path Parameters**:
  - `user_id` (integer): ID of the user to delete (required)
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `message` (string): Deletion success message

### 6. Save User Entries

- **Endpoint**: `/user/entries/`
- **Method**: `POST`
- **Request Body**:
  - `text` (string): Entry text (required)
  - `tags` (list): List of entry tags
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `id` (integer): ID of the created entry
  - `text` (string): Entry text
  - `tags` (list): List of entry tags
  - `date` (string): Current date
  - `time` (string): Current time

### 7. Get User Entries

- **Endpoint**: `/user/entries/`
- **Method**: `GET`
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - List of entry objects:
    - `id` (integer): ID of the entry
    - `text` (string): Entry text
    - `tags` (list): List of entry tags
    - `date` (string): Current date
    - `time` (string): Current time

### 8. Get Entry Details

- **Endpoint**: `/user/entries/{entry_id}/`
- **Method**: `GET`
- **Path Parameters**:
  - `entry_id` (integer): ID of the entry to retrieve (required)
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `id` (integer): ID of the entry
  - `text` (string): Entry text
  - `tags` (list): List of entry tags
  - `date` (string): Current date
  - `time` (string): Current time

### 9. Update Entry

- **Endpoint**: `/user/entries/{entry_id}/`
- **Method**: `PUT`
- **Path Parameters**:
  - `entry_id` (integer): ID of the entry to update (required)
- **Request Body**:
  - `text` (string): New entry text (required)
  - `tags` (list): New list of entry tags
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `id` (integer): ID of the updated entry
  - `text` (string): New entry text
  - `tags` (list): New list of entry tags
  - `date` (string): Current date
  - `time` (string): Current time

### 10. Delete Entry

- **Endpoint**: `/user/entries/{entry_id}/`
- **Method**: `DELETE`
- **Path Parameters**:
  - `entry_id` (integer): ID of the entry to delete (required)
- **Headers**:
  - `Authorization` (string): JWT access token (required)
- **Response**:
  - `message` (string): Deletion success message



Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please create an issue or submit a pull request.

License

This project is licensed under the MIT License.