# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Pre-requisites and local development

Here we have used postgres as a database, so postgres must be installed beforehand with database Trivia.

To start postgres server run `pg_ctl -D C:\postgres\data start`

Create a database named `trivia` using pgAdmin4

There is a file to create tables and populate the tables

- trivia.psql

on a bash terminal you can run the following files using the commands:

```
psql -U _beast101_ -d trivia -h localhost -p 5432 -f trivia.psql
```
### Frontend
The frontend is built using React.js framework. All the packages required are already mentioned in the packages.json file

First install all the required packages for react:

Note: node.js needs to be installed first (<a href=https://nodejs.org/en/download>Download Node JS from Here</a>)<br>
Install the required packages using the following command.
`npm install`

Start the react application using: `npm start`

By default the frontend will run on `localhost:3000`

### Backend
The backend is built on flask framework.
Before getting started, these dependencies need to be installed:
  - Python 3.11 (You can refer this <a href=https://www.python.org/downloads/>Link</a>)
  
  - Virtual Environment (Set up a virtual environment for your app to keep the dependencies and packages exclusive to the current project <a href=https://pypi.org/project/virtualenv/>Read More Here</a>)<br/>
  
To install virtual environment, use the python package installer pip: `pip install virtualenv`<br/>
Create a virtual env folder `python -m venv venv`<br/>
Redirect to the folder containing `venv` folder.<br/>
on Windows use command `venv\Scripts\activate` to activate virtual env

  - Now since virtual environment is setup, lets install the dependencies required for Trivia App
    
All the required packages are in the requirements.txt.

```
pip install -r requirements.txt
```

IMPORTANT DEPENDENCY:
  - python-dotenv (`pip install python-dotenv`) This package is used to read the `.env` file which stores the secret database values i.e. DB_USER, DB_HOST, DB_PASSWORD, DB_NAME

By default, the backend server will run on `127.0.0.1:5000`. This has been added as proxy on package.json file

To run the flask server run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --debug
```
The development environment ensures the server restarts when any changes is detected and --debug is used to run server with debugging mode on.

### Add the node modules folder and venv folder or all the cache files and settings files to .gitignore file

### Testing
Testing is important for a test-driven development. All the tests to verify the endpoints are stored in the test_flaskr.py file in the backend folder.<br>

Navigate to the backend folder.<br>
Create a database using `trivia_test` database using pgAdmin4<br>
Populate it with `psql trivia_test < trivia.psql`<br>
Run the test file using `python test_flaskr.py`


## API Reference

### Getting Started
The Trivia App is built keeping in mind REST protocol. This API contains endpoints to add new question, categories, delete question, sort questions by categories, search questions and play quiz. This API accepts form-encoded requests and returns with JSON-encoded reponses using standard HTTP response codes and authentication.

Base URL:
  - base url: `http://127.0.0.1:5000/`
At the moment, since this app is not hosted, it can only be run locally. Also this url is set as proxy in the frontend configuration.

Authentication:
  - This version of app doesn't require API keys or authentication.

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
  - 404 (Not Found)
  - 422 (Unprocessable)

### Endpoints

### Show Categories Endpoint: `GET /categories`

Sample Request: `curl http://127.0.0.1:5000/categories`

Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

### Show Questions Endpoint: `GET /questions`

Sample Request: `curl 127.0.0.1:5000/questions`

Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "page": 1,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": null
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": null
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "rating": 4
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "rating": null
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?",
      "rating": null
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "rating": null
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "rating": null
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?",
      "rating": null
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "rating": null
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "rating": null
    }
  ],
  "success": true,
  "total_questions": 20
}

```

### Add New Questions Endpoint: `POST /questions/add`

Sample Request: `curl -X POST http://127.0.0.1:5000/questions/add -H "Content-Type: application/json" -d '{ "question": "When does United States of America Celebrate their Independence Day?", "answer": "July 4", "difficulty": 2, "category": 3, "rating": 4}'`

Response:
```
{
  "success": true,
  "total_questions": 21
}
```

### Add New Category Endpoint: `POST /categories/add`

Sample Request: `curl -X POST http://127.0.0.1:5000/categories/add -H "Content-Type: application/json" -d '{ "category": "Music"}'`

Response:
```
{
  "success": true,
  "total_categories": 7
}
```

### Delete the Question Endpoint: `DELETE /questions/<int:question_id>`

Sample Request: `curl -X DELETE http://127.0.0.1:5000/questions/25`

Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Music"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": null
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": null
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "rating": 4
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "rating": null
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?",
      "rating": null
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "rating": null
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "rating": null
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?",
      "rating": null
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "rating": null
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "rating": null
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### Search Questions Endpoint: `POST /questions`

Sample Request: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{ "searchTerm": 'soccer'}'` 

Response:
```
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
      "rating": null
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

### Get Questions By Category Endpoint: `GET /categories/<int:category_id>/questions`

Sample Request: `curl http://127.0.0.1:5000:/categories/3/questions`

Response:
```
{
  "currentCategory": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "rating": null
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "rating": null
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "rating": null
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```

### Play Game Endpoint: `POST /quizz`

Sample Request: `curl -X POST http://127.0.0.1:5000/quizz -H "Content-Type: application/json" -d '{ "previous_questions":[2, 4], "quiz_category": {"type": "Entertainment", "id": "5"}}'`

Response:
```
{
  "question": {
    "answer": "Edward Scissorhands",
    "category": 5,
    "difficulty": 3,
    "id": 6,
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
    "rating": null
  },
  "success": true
}
```

## Deployment
Deployment is not applicable here since the app is hosted locally

## Authors
The starter code was created by Udacity team.

Benson P Sabu worked on:
  - backend files
      - __init__.py
      - models.py
      - test_flaskr.py
      - .env
  - frontend files
      - FormView.js
      - Question.js
      - QuestionView.js
      - QuizView.js

## Acknowledgements
All the instructors especially Caryn and the mentors at Knowledge community did a wonderful job in guiding the students with the content of the course and help with stuck at some problem.

