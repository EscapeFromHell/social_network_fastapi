# Social Network FastAPI
This is a web service that allows you to view users posts, create, edit and delete your own posts, 
like and dislike posts made by other users.

## Features
- User Registration: Allows users to register by providing their username, email, and password.
- User Authentication: Provides user authentication using JWT (JSON Web Tokens).
- User Profile: Provides user profile information.
- View Posts: Allows users, including unregistered users, to view posts.
- Post Creation: Enables users to create new posts by providing the post text.
- Post Editing: Allows users to edit their own posts by providing the updated post text.
- Post Deletion: Enables users to delete their own posts.
- Post Like/Dislike: Allows users to like or dislike posts. You cannot like or dislike your own posts.
- Integration with ClearBit API to retrieve additional information about users (if the email is present in the ClearBit database)
- Integration with EmailHunter API for email verification and validation.

## Technologies
Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, Docker

## Getting Started
To run the project locally, follow these steps:

- Download the project: 
```
git clone https://github.com/EscapeFromHell/social_network_fastapi.git
```
- After downloading the project, navigate to the project folder: 
```
cd social_network_fastapi
```
- Execute the command to create .env file: 
```
cp .env.example .env
```

- To work with the ClearBit API and EmailHunter API, you need to get the API Keys 
on the sites ```https://clearbit.com``` / and ```https://emailhunter.co``` / and register the received API Keys in the 
```.env``` file. If the keys are not specified, the service will work without the functionality of ClearBit and EmailHunter.

- Execute the command: 
```
docker compose up -d --build
```
- Once the containers are up and running, the API documentation will be accessible at: http://127.0.0.1:8000/docs

## Authorization
To authorize the user, you need to register a new user through SignUp endpoint ```POST /api_v1/auth/signup```, then click on the Authorize button in the top
right corner and enter the username and password of the registered user. After successful authorization, you can use
```GET /api_v1/auth/me``` to retrieve information about the currently authorized user.

## API Endpoints
The following API endpoints are available:

- ```POST /api_v1/auth/signup```: Signup (You can use the email alex@clearbit.com to check the integration with the ClearBit API).
- ```POST /api_v1/auth/login```: Create an access token.
- ```GET /api_v1/auth/me```: Get current user profile.
- ```GET /api_v1/posts```: Get all posts.
- ```POST /api_v1/posts```: Create a new post.
- ```PUT /api_v1/posts```: Edit an existing post.
- ```DELETE /api_v1/posts```: Delete an existing post.
- ```POST /api_v1/posts/like```: Like a post.
- ```POST /api_v1/posts/dislike```: Dislike a post.

For detailed information about the request and response formats, refer to the API documentation.
