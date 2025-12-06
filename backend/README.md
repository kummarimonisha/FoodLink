This is the backend service for the FoodLink project. The backend handles authentication (JWT-based), user roles, and donation management.

Technologies Used:

| Component         | Technology               |
| ----------------- | ------------------------ |
| Backend Framework | Flask (Python)           |
| Database          | SQLite (local)           |
| Auth System       | JWT (Flask-JWT-Extended) |
| ORM               | SQLAlchemy               |
| API Testing       | Thunder Client / Postman |

SETUP INSTRUCTIONS:

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


Authentication Endppoints:

| Method | Endpoint             | Description             | Auth Required |
| ------ | -------------------- | ----------------------- | ------------- |
| POST   | `/api/auth/register` | Create a new user       | ❌            |
| POST   | `/api/auth/login`    | Login and get JWT token | ❌            |
| GET    | `/api/auth/me`       | Get logged user info    | ✔ JWT         |


After login → Copy token and include it in Authorization header:

Authorization: Bearer <token>

---------------------------------------------------------------------------------------

Example Testing Flow (Thunder Client / Postman)

1. Register a user
2. Login → copy access_token
3. Use token to call:

GET http://127.0.0.1:5000/api/auth/me


Select Headers tab → Add:

Key	Value
Authorization	Bearer eyJhbGciOiJI...

If successful, you will see:

{
  "message": "Current user",
  "user_id": "1"
}