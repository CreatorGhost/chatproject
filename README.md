 

# Django Chat Application

This is a real-time chat application built with Django, Django Channels, and Redis.

## Features

- User registration and authentication
- Real-time chat functionality with WebSocket
- User status tracking (online/offline)
- Friend recommendation based on user interests and age
- RESTful API endpoints for user registration, login, logout, profile update, and more

## Installation

1. Clone the repository:
```
git clone https://github.com/CreatorGhost/chatproject.git
```
2. Install the requirements:
```
pip install -r requirements.txt
```
3. Apply the migrations:
```
python manage.py migrate
```
4. Run the server:
```
daphne chatproject.asgi:application  
```

## Usage

- Register a new user at `/api/register/`
- Log in at `/api/login/`
- Start a chat at `/api/start-chat/`
- Send a message at `/api/send-message/`
- Get recommended friends at `/api/suggested-friends/<user_id>/`
- Get online users at `/api/online-users/`

## Testing

Run the tests with:
```
python manage.py test
```