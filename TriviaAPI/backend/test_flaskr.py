import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flaskr import create_app
from models import setup_db, Question, Category, db

load_dotenv()
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = f"postgresql://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}@{os.getenv('TEST_DB_HOST')}/{os.getenv('TEST_DB_NAME')}"
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        
#-----------------------------------------------------------------------------------------------!
        #setup_db(self.app, self.database_path)
    
    
        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
        
    # This section of code is not required since Flask has already 
    # created an instance of SQLAlchemy
#-----------------------------------------------------------------------------------------------!
    
    def tearDown(self):
        """Executed after reach test"""
        pass
#-----------------------------------------------------------------------------------------------!
# @TODO: Write at least one test for each test for successful operation and for expected errors.
# completed
#-----------------------------------------------------------------------------------------------!

#-----------------------------------------------------------------------------------------------!
# Test to check if we can get all the categories to display
#-----------------------------------------------------------------------------------------------!
    def test_check_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)
    
#-----------------------------------------------------------------------------------------------!
# Test to check if it returns all the questions and those questions are paginated
#-----------------------------------------------------------------------------------------------!
    def test_paginate_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'],19)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
    
#-----------------------------------------------------------------------------------------------!
# Test to check if the unreachable requested page for getting questions returns 404 error
#-----------------------------------------------------------------------------------------------!
    def test_404_for_unreachable_page(self):
        res = self.client().get('/questions?page=13')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Resource Not Found')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if new questions are added
#-----------------------------------------------------------------------------------------------!
    def test_add_new_question(self):
        res = self.client().post('/questions/add', json={'question': 'India Independence Day', 'answer': 'August 15', 'difficulty': 2, 'category': 4})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
#-----------------------------------------------------------------------------------------------!
# Test to check if while adding new questions, for incomplete json data should return 422 error
#-----------------------------------------------------------------------------------------------! 
    def test_422_unprocessable_new_question(self):
        res = self.client().post('/questions/add', json={'question': 'India Independence Day'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable error')
        
#-----------------------------------------------------------------------------------------------!
# Test to check if new category is added
#-----------------------------------------------------------------------------------------------!
    def test_add_new_category(self):
        res = self.client().post('/categories/add', json={'category': 'Music'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
#-----------------------------------------------------------------------------------------------!
# Test to check if while adding new category, for incomplete json data should return 422 error
#-----------------------------------------------------------------------------------------------! 
    def test_422_unprocessable_new_category(self):
        res = self.client().post('/categories/add')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Unprocessable error')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if questions can be deleted
#-----------------------------------------------------------------------------------------------!
    def test_delete_question(self):
        res = self.client().delete('/questions/24')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'],19)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
    
#-----------------------------------------------------------------------------------------------!
# Test to check if the requested question to be deleted exists or return error 404
#-----------------------------------------------------------------------------------------------!   
    def test_404_question_to_be_deleted_doesnt_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if the displayed questions by categories are of the same categories
#-----------------------------------------------------------------------------------------------!
    def test_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['totalQuestions'],4)
        self.assertEqual(data['currentCategory'],'Art')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if requested category is out of range and return error 404
#-----------------------------------------------------------------------------------------------!
    def test_404_questions_by_category_out_of_range(self):
        res = self.client().get('/categories/20/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if question can be searched using substring
#-----------------------------------------------------------------------------------------------!
    def test_find_question_by_substring(self):
        res = self.client().post('/questions', json={'searchTerm': 'soccer'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['totalQuestions'],2)
    
#-----------------------------------------------------------------------------------------------!
# Test to check if question cannot be found/searched using the substring
#-----------------------------------------------------------------------------------------------!  
    def test_404_cant_find_question_by_substring(self):
        res = self.client().post('/questions', json={'searchTerm': 'history'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Resource Not Found')
    
#-----------------------------------------------------------------------------------------------!
# Test to check if quiz can be played
#-----------------------------------------------------------------------------------------------!
    def test_if_you_can_play_quiz(self):
        res = self.client().post('/quizz', json={'previous_questions': [], 'quiz_category': {'type': 'Sports', 'id': 6}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
#-----------------------------------------------------------------------------------------------!
# Test to check if quiz with no quiz_category data returns error 422
#-----------------------------------------------------------------------------------------------!
    def test_cannot_play_quiz(self):
        res = self.client().post('/quizz', json={'previous_questions': []})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()