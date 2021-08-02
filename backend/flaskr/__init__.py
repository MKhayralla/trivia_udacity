import os
from flask import Flask, request, abort, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import choice
from werkzeug.exceptions import NotFound

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(questions=[], page_number=1, chunk_size=QUESTIONS_PER_PAGE):
    '''
    handles pagination of questions
    '''
    start = (page_number - 1) * chunk_size
    end = start + chunk_size
    res = questions[start:end]
    return res


def call_function(kwargs, fun):
    '''
    calls a function fun on a dict kwargs as long as the value is not None
    '''
    return fun(**{k: v for k, v in kwargs.items() if v is not None})


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
    cors = CORS(app, send_wildcard=True)

    @app.after_request
    def add_headers(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, DELETE')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:3000')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            response = {
                'success': True,
                'categories': {c.id: c.type for c in categories},
                'total_categories': len(categories)
            }
            return jsonify(response)
        except :
            abort(500)
        

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.
  '''
    @app.route('/questions', methods=['GET', 'POST'])
    def question_actions():
        if request.method == 'GET':
            response = {}
            kwargs = {}
            kwargs['page_number'] = request.args.get('page', type = int)
            questions = Question.query.all()
            kwargs['questions'] = [q.format() for q in questions]
            response['success'] = True
            result = call_function(kwargs, paginate_questions)
            if len(result) == 0:
                abort(404)
            response['questions'] = result
            response['total_questions'] = len(questions)
            response['categories'] = {
                c.id: c.type for c in Category.query.all()
                }
            response['current_category'] = None
        else:
            data = request.json
            if 'searchTerm' in data:
                response = {}
                kwargs = {}
                kwargs['page_number'] = request.args.get('page')
                questions = Question.query.filter(
                    Question.question.ilike('%{}%'.format(data['searchTerm']))
                ).all()
                kwargs['questions'] = [q.format() for q in questions]
                response['success'] = True
                response['questions'] = call_function(kwargs, paginate_questions)
                response['total_questions'] = len(questions)
                response['current_category'] = None
            else:
                try:
                    new_question = Question(**data)
                    new_question.insert()
                except :
                    abort(422)
                response = {
                    'success': True,
                    'question_id': new_question.id,
                    'total_questions': Question.query.count()
                }
        return jsonify(response)

    '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  '''
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            q = Question.query.filter_by(id=q_id).first_or_404(description = 'no book with this ID found')
            page = request.args.get('page', 1, type = int)
            q.delete()
            questions = [q.format() for q in Question.query.all()]
        except NotFound as e:
            abort(404)   
        except:
            abort(422)
        response = {
            'success': True,
            'deleted_question_id': q_id,
            'questions' : paginate_questions(questions, page),
            'total_questions': len(questions)
            }
        return jsonify(response)

        
        
    '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        response = {}
        kwargs = {}
        try:
            kwargs['page_number'] = request.args.get('page', 1, int)
        except:
            abort(422)
        categories = [c.id for c in Category.query.all()]
        if category_id not in categories:
            abort(404, description = 'category not found')
        questions = Question.query.filter(
            Question.category == category_id).all()
        kwargs['questions'] = [q.format() for q in questions]
        response['success'] = True
        response['questions'] = call_function(kwargs, paginate_questions)
        response['total_questions'] = len(questions)
        response['current_category'] = Category.query.filter(
            Category.id == category_id).one().type
        return jsonify(response)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            return get_next_question()
        except NotFound as e:
            abort(404, description = e.description)
        except Exception as e:
            abort(422)
    def get_next_question():
        query = request.json
        category_id = int(query['quiz_category'].get('id'))
        result = [q.format() for q in Question.query.all()]
        response = {
            'success': True
        }
        categories = [c.id for c in Category.query.all()]
        if category_id not in categories and category_id != 0:
            abort(404, description = 'category not found')
        if category_id == 0:
            choices = result
        else:
            choices = list(
                filter(lambda x: x['category'] == category_id, result))
        done = query['previous_questions']
        filtered_result = [q for q in choices if q['id'] not in done]
        if len(filtered_result) > 0:
            response['question'] = choice(filtered_result)
        return jsonify(response)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource Not Found',
            'error': 404
        }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            'success': False,
            'message': 'Unprocessable Request',
            'error': 422
        }), 422
    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
            'success': False,
            'message': 'Method Not Allowed',
            'error': 405
        }), 405
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal Server Error',
            'error': 500
        }), 500
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad Request',
            'error': 400
        }), 400
    return app
