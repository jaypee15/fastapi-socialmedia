# API for a social media application 



## Features:

- Fast and Asynchronous: Built on the asynchronous FastAPI framework, the API ensures lightning-fast response times and efficient handling of concurrent requests.

- User Authentication: Secure user authentication powered by JWT tokens, ensuring a safe and seamless experience for users.

- Post Management: Create, read, update,delete, like and unlike posts with.

- API Documentation: Automatically generated OpenAPI and JSON Schema documentation, ensuring ease of integration and development.

#### The API  has 3 main routes

## 1) Post route

#### This route is reponsible for creating posts, deleting post by ID, updating post and reading posts.

## 2) Users route

#### This route is used for authentication and authorization with endpoints for creating users, getting user by email, login users, get the current logged in user details and logging out users.


## 3) Like route

 #### This route is allows authenticaated users to like or unlike any post.

# how to run locally
Clone this repo by using following command
````
git clone git@github.com:jaypee15/fastapi-socialmedia.git
````
then 

````
cd fastapi-socialmedia
````

Then install all dependencies and packages 

````
pip install -r requirements.txt
````

Run follwoing command to start the gunicorn server.

````
uvicorn app:main:app --reload
````

Then you can use following link to access the API docs and play around with it.

````
http://127.0.0.1:8000/docs 

````

## Set up database.
Create a .env file and add the following.

````
DATABASE_URL = "sqlite:///sqlite.db"
SECRET_KEY = "09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
````
### Note: The SECRET_KEY in this README is a pseudo key. Get a new secret key for yourself.
 
---
### Database Entity relationship Diagram.

![database ERD](/static/drawSQL-fastapi-social.png)