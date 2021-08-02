#  Full Stack Trivia API 

The project is an educational project and one of udacity full-stack nanodegree projects .
it is a demonstration of API development techniques using flask micro-framework .
most remarakable modules used are SQLAlchemy, flask-cors and unittest .
TDD approach is used through the development life-cycle .
code style in the backend is [PEP8](https://www.python.org/dev/peps/pep-0008/)


## Getting Started

### Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)





2. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


3. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the server

in the backend folder, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


the first line tells flask to look for the start point of the app at flaskr/__init__.py .
the second line is activating development mode to auto reload on change .

### Frontend

1. **Node** - Follow instructions to install the latest version of node.js for your platform in the [Node.js docs](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)





2. **NPM Packages** once you installed node and npm install dependencies by naviging to the `/frontend` directory and running:
```bash
npm install
```
This will install all of the required packages .

#### Running the server

in the frontend folder, execute:

```bash
npm start
```
this will start the frontend app on `http://localhost:3000/`

## Testing The Backend
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Error Handling
The API will respond with a json response that contains error code and failure message

#### Sample error response
```
{
    "success" : false,
    "error" : 404,
    "message" : "Resource Not Found"
}
```

Expected errors are 400,404,405,422,500

### Endpoints

#### GET /categories
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string 
```bash
curl -X GET http://localhost:5000/categories/
```

```json
{
    "success" : true,
    "categories" : {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    },
    "total_categories" : 6
}

```


#### GET /questions
- Request Arguments: `page` argument sets the page returned (starting at page 1 and defaulted to 1)
- Returns: an object conatining key questions with paginated result, key categories with all categories, total_questions  
```bash
curl -X GET http://localhost:5000/questions?page=2
```

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
  "current_category": null, 
  "questions": [
    {
      "answer": "10", 
      "category": 6, 
      "difficulty": 3, 
      "id": 24, 
      "question": "How many times have Al-Ahly won CAF champions league?"
    }, 
    {
      "answer": "5", 
      "category": 6, 
      "difficulty": 2, 
      "id": 29, 
      "question": "How many times have Brazil won the World Cup in football ? "
    }, 
    {
      "answer": "Lose Yourself", 
      "category": 5, 
      "difficulty": 3, 
      "id": 30, 
      "question": "What is the Eminem Song that won the Oscar ?"
    }
  ], 
  "success": true, 
  "total_questions": 13
}

```

#### GET /categories/<int:category_id>/questions
- Request Arguments: `page` argument sets the page returned (starting at page 1 and defaulted to 1)
- Returns: an object conatining key category questions with paginated result, key categories with all categories, total_questions  
```bash
curl -X GET http://localhost:5000/categories/6/questions
```

```json
{
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "10", 
      "category": 6, 
      "difficulty": 3, 
      "id": 24, 
      "question": "How many times have Al-Ahly won CAF champions league?"
    }, 
    {
      "answer": "5", 
      "category": 6, 
      "difficulty": 2, 
      "id": 29, 
      "question": "How many times have Brazil won the World Cup in football ? "
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```

#### POST /questions
- Request Arguments: None
- Posts new question to the database
- Payload: `question`, `answer`, `difficulty`, `category`

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"question":"Who is Einestein ?","answer":"A scientist","category":"1","difficulty":"1"}' http://localhost:5000/questions

```

```json
{
    "question_id": 31, 
    "success": true, 
    "total_questions": 14
}
```

#### POST /questions
- Request Arguments: None
- search questions using a search term
- Payload: `searchTerm` (case insensitive)

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"searchTerm":"ahly"}' http://localhost:5000/questions

```

```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "10", 
      "category": 6, 
      "difficulty": 3, 
      "id": 24, 
      "question": "How many times have Al-Ahly won CAF champions league?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### DELETE /questions/<int:question_id>
- Request Arguments: `page` argument sets the page returned (starting at page 1 and defaulted to 1)
- Deletes the question with the given question_id

```bash
curl -X DELETE  http://localhost:5000/questions/12?page=2

```

```json
{
  "deleted_question_id": 12, 
  "questions": [
    {
      "answer": "5", 
      "category": 6, 
      "difficulty": 2, 
      "id": 29, 
      "question": "How many times have Brazil won the World Cup in football ? "
    }, 
    {
      "answer": "Lose Yourself", 
      "category": 5, 
      "difficulty": 3, 
      "id": 30, 
      "question": "What is the Eminem Song that won the Oscar ?"
    }
  ], 
  "success": true, 
  "total_questions": 12
}

```

#### POST /quizzes
- Request Arguments: None
- get new quiz question in a specific category or all categories or none if there is no remaining questions
- Payload: `previous_questions` (an array of previous questions ID's), `quiz_category`

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"quiz_category":{"id":"6"},"previous_questions":[24]}' http://localhost:5000/quizzes

```

```json
{
  "question": {
    "answer": "5", 
    "category": 6, 
    "difficulty": 2, 
    "id": 29, 
    "question": "How many times have Brazil won the World Cup in football ? "
  }, 
  "success": true
}

```

## Authors
- Mahmoud Khayralla (Me)
- Udacity team who made the starter code of this project which you can find [here](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter)

## Acknowledgements
- I would like to thank the instructor  for making things very simple to make and work with Flask API's
- I'd like to thank [Udacity](http://udacity.com/) for their great contribution to the IT learning community
- I'd like to thank the [NTL_initiative](http://techleaders.eg/learning-tracks/) for giving me this chance