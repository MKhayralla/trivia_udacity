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

    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            q = Question.query.filter_by(id=q_id).first_or_404(description = 'No Question With This ID Found')
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
