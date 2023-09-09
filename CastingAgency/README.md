# Capstone Casting Agency Final Project

## Casting Agency Application

An application where one can add actors or movies to the database with appropriate permissions is the "CASTING AGENCY" application


## Pre-requisites and local development

Here we have used postgres as a database, so postgres must be installed beforehand with database Trivia.

To start postgres server run `pg_ctl -D C:\postgres\data start`

Create a database named `capstone` using pgAdmin4
Create a database named `test_capstone` using pgAdmin4

There is a file to create tables and populate the tables one foe main database and other for test database

- capstone_backup.psql
- test_capstone_backup.psql

on a bash terminal you can run the following files using the commands:

```
psql -U postgres -d capstone -h localhost -p 5432 -f capstone_backup.psql
```
```
psql -U postgres -d test_capstone -h localhost -p 5432 -f test_capstone_backup.psql
```
### Auth0 Authentication
Auth0 is an authentication service provider for login and logout requirements for applications that also provides ability to create roles, permissions etc. to use in our application.<br/>
Now the login URL is 
```
https://capstone-fsnd-1234.us.auth0.com/authorize?audience=casts&response_type=token&client_id=pWJFyxY4bglHX7UXThOfnPif5XquA29g&redirect_uri=http://127.0.0.1:5000
```
You will get a login page where you can generate access token.<br/>
The created users i.e 
- Cast Assistant,
- Cast Director,
- Executive Producer<br/>

and its credentials are placed in the .env file.

### Backend
The backend is built on flask framework.
Before getting started, these dependencies need to be installed:
  - Python 3.11 (You can refer this <a href=https://www.python.org/downloads/>Link</a>)
  
  - Virtual Environment (Set up a virtual environment for your app to keep the dependencies and packages exclusive to the current project <a href=https://pypi.org/project/virtualenv/>Read More Here</a>)<br/>
  
To install virtual environment, use the python package installer pip: `pip install virtualenv`<br/>
Create a virtual env folder `python -m venv venv`<br/>
Redirect to the folder containing `venv` folder.<br/>
on Windows use command `venv\Scripts\activate` to activate virtual env

  - Now since virtual environment is setup, lets install the dependencies required for Casting Agency App
    
All the required packages are in the requirements.txt.

```
pip install -r requirements_not_render.txt
```
This is because render runs on python 3.7 and our project is in python 3.11.

MODELS USED HERE are <br/>
 - Movies
 - Actors

These models are in a one to many relationship since an actor_id is required to create a new movie<br/>

Attributes in the movies table are:<br/>
 - id
 - title
 - release_date
 - genre
 - actor_id
   
Attributes in the actors table are:<br/>
 - id
 - name
 - age
 - gender

IMPORTANT DEPENDENCY:
  - python-dotenv (`pip install python-dotenv`) This package is used to read the `.env` file which stores the secret database values i.e. DB_USER, DB_HOST, DB_PASSWORD, DB_NAME
  - .env file consists of all the necessary environment variable to access the app

By default, the backend server will run on `127.0.0.1:5000`.

To run the flask server run the following commands:
```
python app.py
```

### Add the venv folder or all the cache files and settings files to .gitignore file

### Testing
Testing is important for a test-driven development. All the tests to verify the endpoints are stored in the test_app.py file in the backend folder.<br>

Navigate to the backend folder.<br>
Create a database using `test_capstone` database using pgAdmin4<br>
Populate it with `psql test_capstone < capstone_backup.psql`<br>
Run the test file using `python test_app.py`


## API Reference

### Getting Started
The Casting Agency App is built keeping in mind REST protocol.<br/>
This application contains endpoints to add new actors, movies, delete an actor or movie, update and get actor or movies<br/>
This API accepts json-encoded requests and returns with JSON-encoded reponses using standard HTTP response codes and authentication.

## Base URL:
  - base url: `http://127.0.0.1:5000/`
  - base url for render `https://render-capstone-backend.onrender.com` 
At the moment this app is hosted on render, it can also be run locally.

## Authentication:
There are 3 users to check the authentication
  - Casting Assistant
  - Casting Director
  - Executive Producer.<br/>

The user access_tokens are provided in .env file.

### Error Handling
Error are handled using the `@app.errorhandler` decorator which returns json as follows:
```
{
  'success': False,
  'error': 404,
  'message': 'Resource not Found.'
}
```

The error codes being handled here in this app are:
  - 400 (Bad Request)
  - 401 (Forbidden)
  - 403 (Unauthorized)
  - 404 (Not Found)
  - 422 (Unprocessable)
  - 500 (Server Error)
  - AuthError

### Endpoints

### Show Movies Endpoint: `GET /movies`

Sample Request: 
```
curl -X GET https://render-capstone-backend.onrender.com/movies -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w"
```

Response:
```
{
  "movies_dict": [
    {
      "actor_id": 3,
      "genre": "SciFi",
      "id": 1,
      "release_date": "10/06/2018",
      "title": "Avengers"
    },
    {
      "actor_id": 2,
      "genre": "Action",
      "id": 2,
      "release_date": "20/10/2019",
      "title": "John Wick"
    },
    {
      "actor_id": 1,
      "genre": "Action",
      "id": 3,
      "release_date": "15/02/2023",
      "title": "Mission Impossible 6"
    }
  ],
  "success": true
}
```

### Show Actors Endpoint: `GET /actors`

Sample Request: 
```
curl -X GET https://render-capstone-backend.onrender.com/actors -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w"
```

Response:
```
{
    "actors_dict": [
        {
            "age": 60,
            "gender": "male",
            "id": 1,
            "name": "Tom Cruise"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "Keanu Reeves"
        },
        {
            "age": 40,
            "gender": "female",
            "id": 3,
            "name": "Scarlett Johanssen"
        }
    ],
    "success": true
}
```

### Post New Actor Endpoint: `POST /actors`

Sample Request: 
```
curl -X POST https://render-capstone-backend.onrender.com/actors \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w" \
-H "Content-Type: application/json" \
-d '{
    "age": 50,
    "gender": "male",
    "id": 4,
    "name": "Johnny Depp"
}'
```

Response:
```
{
    "actors_dict": [
        {
            "age": 60,
            "gender": "male",
            "id": 1,
            "name": "Tom Cruise"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "Keanu Reeves"
        },
        {
            "age": 40,
            "gender": "female",
            "id": 3,
            "name": "Scarlett Johansson"
        },
        {
            "age": 50,
            "gender": "male",
            "id": 4,
            "name": "Johnny Depp"
        }
    ],
    "success": true
}
```

### Add New Movie Endpoint: `POST /movies`

Sample Request: 
```
curl -X POST https://render-capstone-backend.onrender.com/movies \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w" \
-H "Content-Type: application/json" \
-d '{
      "actor_id": 4,
      "genre": "Action",
      "id": 3,
      "release_date": "15/02/2023",
      "title": "Pirates of the Caribean 6"
    }'
```

Response:
```
{
    "movies_dict": [
        {
            "actor_id": 3,
            "genre": "SciFi",
            "id": 1,
            "release_date": "10/06/2018",
            "title": "Avengers"
        },
        {
            "actor_id": 2,
            "genre": "Action",
            "id": 2,
            "release_date": "20/10/2019",
            "title": "John Wick"
        },
        {
            "actor_id": 1,
            "genre": "Action",
            "id": 3,
            "release_date": "15/02/2023",
            "title": "Mission Impossible 6"
        },
        {
            "actor_id": 4,
            "genre": "Action",
            "id": 4,
            "release_date": "15/02/2023",
            "title": "Pirates of the Caribbean 6"
        }
    ],
    "success": true,
    "total_movies": 4
}
```

### Update the Movie Endpoint: `PATCH /movies/<int:movie_id>`

Sample Request: 
```
curl -X PATCH https://render-capstone-backend.onrender.com/movies/4 \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w" \
-H "Content-Type: application/json" \
-d '{
      "actor_id": 4,
      "genre": "Action",
      "id": 3,
      "release_date": "22/05/2020",
      "title": "Pirates of the Caribbean 6"
    }'
```

Response:
```
{
    "Movie_updated": {
        "actor_id": 4,
        "genre": "Action",
        "id": 4,
        "release_date": "22/05/2020",
        "title": "Pirates of the Caribbean 6"
    },
    "movies_dict": [
        {
            "actor_id": 3,
            "genre": "SciFi",
            "id": 1,
            "release_date": "10/06/2018",
            "title": "Avengers"
        },
        {
            "actor_id": 2,
            "genre": "Action",
            "id": 2,
            "release_date": "20/10/2019",
            "title": "John Wick"
        },
        {
            "actor_id": 1,
            "genre": "Action",
            "id": 3,
            "release_date": "15/02/2023",
            "title": "Mission Impossible 6"
        },
        {
            "actor_id": 4,
            "genre": "Action",
            "id": 4,
            "release_date": "22/05/2020",
            "title": "Pirates of the Caribbean 6"
        }
    ],
    "success": true
}
```

### Update Actor Endpoint: `PATCH /actors/<int:actor_id>`

Sample Request: 
```
curl -X PATCH https://render-capstone-backend.onrender.com/actors/4 \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w" \
-H "Content-Type: application/json" \
-d '{
            "age": 55,
            "gender": "male",
            "id": 4,
            "name": "Johnny Depp"
        }'
```

Response:
```
{
    "actor_updated": {
        "age": 55,
        "gender": "male",
        "id": 4,
        "name": "Johnny Depp"
    },
    "actors_dict": [
        {
            "age": 60,
            "gender": "male",
            "id": 1,
            "name": "Tom Cruise"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "Keanu Reeves"
        },
        {
            "age": 40,
            "gender": "female",
            "id": 3,
            "name": "Scarlett Johanssen"
        },
        {
            "age": 55,
            "gender": "male",
            "id": 4,
            "name": "Johnny Depp"
        }
    ],
    "success": true
}
```

### Delete Movie Endpoint: `DELETE /movies/<int:movie_id>`

Sample Request: 
```
curl -X DELETE https://render-capstone-backend.onrender.com/movies/4 \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w"
```

Response:
```
{
    "deleted_movie_title": "Pirates of the Caribbean 6",
    "movies_dict": [
        {
            "actor_id": 3,
            "genre": "SciFi",
            "id": 1,
            "release_date": "10/06/2018",
            "title": "Avengers"
        },
        {
            "actor_id": 2,
            "genre": "Action",
            "id": 2,
            "release_date": "20/10/2019",
            "title": "John Wick"
        },
        {
            "actor_id": 1,
            "genre": "Action",
            "id": 3,
            "release_date": "15/02/2023",
            "title": "Mission Impossible 6"
        }
    ],
    "success": true
}
```

### Delete Actor Endpoint: `DELETE /actors/<int:actor_id>`

Sample Request: 
```
curl -X DELETE https://render-capstone-backend.onrender.com/actors/4 \
-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmYWQ2ZGIyZjZmMmU5NDg2OWVmMDIwIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQyNTg4MjUsImV4cCI6MTY5NDM0NTIyNSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.Bq_n_wqH88gaVeQmqtAR-L4Drj2yOBz0O4Fjk6lhe0xPwfCXyhZMPXJctuEvfABey57a4cpb-mB4n-vpBnjG_hBTmTCaBvX5L864iiCveeFrFT8ZJ3WawlKuTzSlPhWMRHHT3ipQzoog7xWXm8F_vsDGltSVouqbBhfcSVBcaPZOg4v5tD_c0t1JAOVguGek_MNZ63HvR-8SPuPp7zbzcePZGrTEIvjQeGy1SOHY4nzaYkreluf2E25Yqha8JQ_UpglwRQ1zqETIBI9WVyB7soG5P-2g_3l7jw1C-KGiY3moHqEwtNIn5TeMWGbQr6u7UPXbfZUcqh8XL6YQULvM1w"
```

Response:
```
{
    "actors_dict": [
        {
            "age": 60,
            "gender": "male",
            "id": 1,
            "name": "Tom Cruise"
        },
        {
            "age": 45,
            "gender": "male",
            "id": 2,
            "name": "Keanu Reeves"
        },
        {
            "age": 40,
            "gender": "female",
            "id": 3,
            "name": "Scarlett Johanssen"
        }
    ],
    "deleted_actor_name": "Johnny Depp",
    "success": true
}
```

## Deployment
App is deployed on render at `https://render-capstone-backend.onrender.com`<br/>
Response if this url is accessed:
```
{
  "success":true
}
```

## Authors
The starter code was created by Benson.

Benson P Sabu worked on:
  - backend files
      - app.py
      - auth.py
      - models.py
      - test_app.py
      - .env
      - capstone_backup.psql
      - test_capstone_backup.psql

## Acknowledgements
All the instructors and the mentors at Knowledge community did a wonderful job in guiding the students with the content of the course and help with stuck at some problem.

