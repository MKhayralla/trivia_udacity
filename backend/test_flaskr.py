import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = 'postgresql://postgres:password@localhost:5432/trivia_test'
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question' : 'Who created 5:40 Train?',
            'answer' : 'Adel Shakal',
            'category' : '1',
            'difficulty' : 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions_correctly(self):
        '''test the paginated questions end point and check if it returns a right formatted result'''
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
    def test_get_questions_404(self):
        '''a page number out of range in questions end point'''
        res = self.client().get('/questions?page=404')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    def test_get_category_questions_success(self):
        '''test category questions end point and check if it returns a right formatted result'''
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        category = Category.query.filter(Category.id == 1).one()
        self.assertEqual(data['current_category'], category.type)
    def test_get_category_questions_404(self):
        '''category not found in category questions end point'''
        res = self.client().get('/categories/404/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    def test_get_categories(self):
        '''test the categories end point and check if it returns a right formatted result'''
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])
    def test_post_question(self):
        '''test adding new question end point'''
        res = self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['question_id'])
    def test_search_question(self):
        '''test adding new question end point'''
        res = self.client().post('/questions', json = {'searchTerm' : 'van'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
    
    def test_delete_question_success(self):
        '''test deleting the created question in the previous test'''
        delete_id = Question.query.first().id
        res = self.client().delete('/questions/{}'.format(delete_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['deleted_question_id'], delete_id)
    def test_delete_question_404(self):
        '''test deleting non-existing question'''
        res = self.client().delete('/questions/404')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_get_next_question_success(self):
        '''test taking quiz successfully retrieving new question'''
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 1},
                                                   'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_get_next_question_last(self):
        '''test taking quiz with all questions done'''
        questions = [q.id for q in Question.query.all()]
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 0},
                                                   'previous_questions': questions})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(data.get('question'))

    def test_get_next_question_category_not_found(self):
        '''test taking quiz in a wrong category'''
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 404},
                                                   'previous_questions': []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_get_next_question_422(self):
        '''test taking quiz not processable'''
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Request')
    
    def test_method_not_allowed(self):
        '''tests a prohibted method error 405'''
        res = self.client().put('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
