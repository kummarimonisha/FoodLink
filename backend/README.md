This is the backend service for the FoodLink project. The backend handles authentication (JWT-based), user roles, and donation workflow.

## Technologies Used:

| Component         | Technology               |
| ----------------- | ------------------------ |
| Backend Framework | Flask (Python)           |
| Database          | SQLite (local)           |
| Auth System       | JWT (Flask-JWT-Extended) |
| ORM               | SQLAlchemy               |
| API Testing       | Thunder Client / Postman |

## Project Structure:

backend/
├── app.py
├── config.py
├── models.py
├── auth_routes.py
├── donation_routes.py
├── security.py
├── email_utils.py
├── requirements.txt
└── README.md

## Setup Instructions:

1. Clone the repository:

git clone https://github.com/kummarimonisha/FoodLink.git
cd FoodLink/backend

2. Create a virtual environment:

python -m venv venv

| OS        | Command                    |
| --------- | -------------------------- |
| Windows   | `venv\Scripts\activate`    |
| Mac/Linux | `source venv/bin/activate` |


3. Install dependencies:

pip install -r requirements.txt

4. Run the backend server

python app.py

The API will be running at: http://127.0.0.1:5000


## Authentication Endpoints - /api/auth/:

| Method | Endpoint                            | Description                                    | Auth Required       |
| ------ | ----------------------------------- | ---------------------------------------------- | ------------------- |
| POST   | `/register`                         | Create a new user account                      | -                   |
| POST   | `/login`                            | Login and receive a JWT token                  | -                   |
| GET    | `/me`                               | Get current logged-in user information         | JWT                 |
| POST   | `/forgot-password`                  | Request password reset link (email simulation) | -                   |
| POST   | `/reset-password`                   | Set new password using reset token             | Reset Token (JWT)   |
| PATCH  | `/profile/update`                   | Update email/username for current user         | JWT                 |
| PATCH  | `/admin/users/<user_id>/deactivate` | Deactivate a user                              | Admin               |
| PATCH  | `/admin/users/<user_id>/activate`   | Activate a user                                | Admin               |

After login → Copy token and include it in Authorization header:      Authorization: Bearer <token>                 

Example Testing Flow (Thunder Client / Postman):

1. Register a user
2. Login → copy access_token
3. Use token to call:

GET http://127.0.0.1:5000/api/auth/me


Select Headers tab/Add:

Key: Authorization
Value: Bearer eyJhbGciOiJI...

If successful, you will see:

{

  "message": "Current user",

  "user_id": "1"

}

## Donations Endpoints - /api/donations/:

| Method | Endpoint                            | Role        | Description                                                    |
| ------ | ----------------------------------- | ------------| ---------------------------------------------------------------|
| POST   | `/`                                 | donor       | Create donation (pending)                                      |
| GET    | `/available`                        | all auth    | List approved + non-expired donations (supports category)      |
| GET    | `/pending`                          | admin       | View pending donations                                         |
| POST   | `/<id>/approve`                     | admin       | Approve donation                                               |
| POST   | `/<id>/reject`                      | admin       | Reject donation                                                |
| POST   | `/<id>/claim`                       | recipient   | Claim donation                                                 |
| POST   | `/admin/users/<user_id>/deactivate` | admin       | Deactivate a user                                              |
| PATCH  | `/api/donations/<id>`               | donor/admin | Edit a pending donation (creator or admin only)                |

## Password Reset Endpoints:

| Método | Endpoint           | Descripción            | Token                |
| ------ | ------------------ | ---------------------- | -------------------- |
| POST   | `/forgot-password` | Enviar link con JWT    | -                    |
| POST   | `/reset-password`  | Guardar nuevo password | Bearer Reset Token   |


## Environment Variables (Optional):

Create a .env file if needed:
JWT_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

## Notes:

- This backend uses simulated emails (printed in console)
- Token expiration for password reset: 10 minutes
- SQLite database auto-generates in project folder