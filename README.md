# Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where I come in! I helped them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=1 && python -m flask run

```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

## API Documentation

### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method not allowed

### Endpoints 
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
{
 "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Muhammadu Buhari",
      "category": 3,
      "difficulty": 2,
      "id": 25,
      "question": "who is president of Nigeria"
    }
  ],
  "total_questions": 21
}
```

`DELETE '/questions/{question_id}`
Deletes a specified question using the id of the question
- Request Arguments: `question_id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question.
Sample: `curl -X DELETE http://127.0.0.1:5000/questions/12`
```json
{
  "deleted": 15,
  "success": true
}

```
`POST '/questions'`
- Sends a post request in order to add a new question
- Returns the id of the created question, success value and total questions.

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "What actor did author Anne Rice denounce, then praise in the role of her beloved Lestat?", "answer": "Tom Cruise", "category": 5, "difficulty": 4}' http://127.0.0.1:5000/questions`

```json
{
  "created": 64,
  "success": true,
  "total_questions": 20
}

```

`POST '/questions'`
- Sends a post request in order to search for a specific question by search term
- Returns: success value, any array of questions, a number of total_questions that met the search term and the current category string
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "better"}' http://127.0.0.1:5000/questions`

```json
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

`GET '/categories/{question_category}>/questions'`
Fetches questions for a cateogry specified by id request argument
- Request Arguments: `question_category` - integer
- Returns: Sucess value, An object with questions for the specified category, total questions, and current category string
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

```json
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Real Madrid",
      "category": 6,
      "difficulty": 3,
      "id": 29,
      "question": "Who won the 2021 UEFA Champions League"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`POST '/quizzes'`
- Sends a post request in order to get the next question
- Takes category and previous question parameters
and returns success value and a random question within the given category, if provided, and that is not one of the previous questions.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 6], "quiz_category": {"type": "Entertainment", "id": "5"}}' http://127.0.0.1:5000/quizzes`

```json
{
  "question": {
    "answer": "Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  "success": true
}
```
## Deployment N/A

## Authors
Yours truly, Student Eddy

## Acknowledgements 
The awesome team at Udacity and all of the teachers and sessions leads, without your guidance, i wouldnt have been able to complete this project! 