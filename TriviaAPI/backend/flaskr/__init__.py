import os, random, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

#-----------------------------------------------------------------------------------------------!
# @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
# Completed

# Create app function
# database_uri is used to use trivia_test database for tests
#-----------------------------------------------------------------------------------------------!
def create_app(database_uri="",test_config=None):
    app = Flask(__name__)
    if database_uri:
        setup_db(app, database_uri)
    else:
        setup_db(app)
    CORS(app)
    
#-----------------------------------------------------------------------------------------------!
# @TODO: Use the after_request decorator to set Access-Control-Allow
# completed
    
# after request function, Allow * for origin is used in this function
#-----------------------------------------------------------------------------------------------!
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        return response

#-----------------------------------------------------------------------------------------------!
# Function to paginate all the questions
# .paginate method takes in 2 arguments
#   - page (we get page argument from below, if none received it defaults to 1)
#   - per_page (this has already been defined as QUESTIONS_PER_PAGE)
# returned list of objects from the above method is appened to question_array 
# after using .format() method from models.py
#-----------------------------------------------------------------------------------------------!
    def paginate_questions(request, current_questions=None):
        page = request.args.get('page', 1, type=int)
        if current_questions:
            question_array = [question.format() for question in current_questions]
        else:
            current_questions = Question.query.order_by(Question.id).paginate(page=page, per_page=QUESTIONS_PER_PAGE)
            question_array = [question.format() for question in current_questions]
        return page, question_array
    
#-----------------------------------------------------------------------------------------------!  
# @TODO: Create an endpoint to handle GET requests for all available categories.
# completed

# get_category_dict() returns a dictionary of categories with id and type as its keys
# the above functions is used in different functions below
#-----------------------------------------------------------------------------------------------!
    def get_category_dict():
        category_dict = {}
        category = Category.query.all()
        for i in range(0, len(category)):
            category_dict[category[i].id] = category[i].type
        return category_dict
    
    @app.route('/categories')
    def show_categories():
        all_categories = get_category_dict()
        return jsonify({
            'success': True,
            'categories': all_categories,
            'total_categories': len(all_categories)
        })

#-----------------------------------------------------------------------------------------------!
# @TODO: Create an endpoint to handle GET requests for questions, 
# including pagination (every 10 questions).This endpoint should return a list of questions, 
# number of total questions, current category, categories.
# completed

# TEST: At this point, when you start the application 
# you should see questions and categories generated, 
# ten questions per page and pagination at the bottom of the screen for two pages.
# Clicking on the page numbers should update the questions.
# completed

# Note: currentCategory is set as None since the frontend requesting the values 
# isn't using the same 
#-----------------------------------------------------------------------------------------------!
    @app.route('/questions')
    def show_questions():
        # get all the categories dict
        all_categories = get_category_dict()
        
        #paginate the questions list
        page, questions_list = paginate_questions(request)
        
        #error for question_list is None
        if len(questions_list) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'questions': questions_list,
                'page': page,
                'total_questions': len(Question.query.all()),
                'categories': all_categories,
                'currentCategory': None  #referred from udacity knowledge
            })
            
#-----------------------------------------------------------------------------------------------!
# @TODO: Create an endpoint to POST a new question, which will 
# require the question and answer text, category, and difficulty score.
# completed

# TEST: When you submit a question on the "Add" tab, the form will clear and the question 
# will appear at the end of the last page of the questions list in the "List" tab.
#-----------------------------------------------------------------------------------------------! 
    @app.route('/questions/add', methods=['POST'])
    def add_new_questions():
        try:
            # get all the data from request
            new_question = request.get_json().get('question', None)
            question_answer= request.get_json().get('answer', None)
            question_difficulty = request.get_json().get('difficulty', None)
            question_category = request.get_json().get('category', None)
            question_rating = request.get_json().get('rating', None)
            
            #check if the requested data is none or abort error 422
            if (new_question is None) or (question_answer is None) or (question_difficulty is None) or (question_category is None) or(question_rating is None):
                abort(422)
            
            #insert new question
            new_question = Question(question=new_question, answer=question_answer, difficulty=question_difficulty, category=question_category, rating=question_rating)
            new_question.insert() # already defined method in models.py
            return jsonify({
                'success': True,
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(422)
            
#-----------------------------------------------------------------------------------------------!
# Added form for inserting a new category into the database
#-----------------------------------------------------------------------------------------------!
    @app.route('/categories/add', methods=['POST'])
    def add_new_category():
        try:
            category = request.get_json().get('category')
            new_category = Category(type=category)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({
                'success': True,
                'total_categories': len(Category.query.all())
            })
        except:
            abort(422)
#-----------------------------------------------------------------------------------------------!
# @TODO: Create an endpoint to DELETE question using a question ID.
# completed

# TEST: When you click the trash icon next to a question, the question will be removed. 
# This removal will persist in the database and when you refresh the page.
#-----------------------------------------------------------------------------------------------!
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_the_question(question_id):
        try:
            #find the question using question_id
            check_question_exists = Question.query.filter(Question.id==question_id).one_or_none()
            
            # if it doesn't exist then abort 404
            # here we use raise RequestError(404) a custom defined error handler
            # as the abort(404) here redirects to abort(422)
            if check_question_exists is None:
                raise RequestError(404)
            
            #delete the question
            check_question_exists.delete()
            all_categories = get_category_dict()
            page, questions_list = paginate_questions(request)
            return jsonify({
                'success': True,
                'questions': questions_list,
                'total_questions': len(Question.query.all()),
                'categories': all_categories,
                'currentCategory': None  #referred from udacity knowledge
            })
        # this except is for the above RequestError
        except RequestError as error:
            abort(error.status)

        except:
            abort(422)
            
#-----------------------------------------------------------------------------------------------!
# @TODO: Create a POST endpoint to get questions based on a search term. It should return any 
# questions for whom the search term is a substring of the question.
# completed

# TEST: Search by any phrase. The questions list will update to include only question 
# that include that string within their question. Try using the word "title" to start.
#-----------------------------------------------------------------------------------------------!
    @app.route('/questions', methods=['POST'])
    def search_questions():
        try:
            # request the searchTerm
            search_term = request.get_json().get('searchTerm')  
            
            # # if requested term is empty return error 422
            if search_term == '':
                abort(404)
             
            # make the term to lowercase and the strip the extra whitespaces around it 
            search_term = search_term.lower().lstrip().rstrip()
            
            # check if the question exists using the searchterm
            # func.lower() is an SQLAlchemy method to lower all the questions to lower case()
            search_question = Question.query.filter(func.lower(Question.question).contains(search_term)).all()
            
            # if searched question doesn't exist abort 400
            if len(search_question) == 0:
                abort(400)
            
            page, question_list = paginate_questions(request, search_question)
            return jsonify({
                'success': True,
                'questions': question_list,
                'totalQuestions': len(question_list),
                'currentCategory': None
            })
        # except Exception as error:
        #     abort(error.status)
        except:
            abort(404)

#-----------------------------------------------------------------------------------------------!
# @TODO: Create a GET endpoint to get questions based on category.
# completed

# TEST: In the "List" tab / main screen, clicking on one of the categories in the left column 
# will cause only questions of that category to be shown.
#-----------------------------------------------------------------------------------------------!
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # request all the categories dictionary
        allCategories = get_category_dict()
        
        # if the requested id doesn't exist abort error 404
        if category_id not in allCategories.keys():
            abort(404)
        try:
            # get all the same category questions using category
            questions_by_category = Question.query.filter(Question.category==category_id).all()
            
            # make a list of the returned questions_by_category object
            question_list = [question.format() for question in questions_by_category]
            return jsonify({
                'success': True,
                'questions': question_list,
                'totalQuestions': len(question_list),
                'currentCategory': allCategories[category_id]
            })
        except:
            abort(422)
            
#-----------------------------------------------------------------------------------------------!
# @TODO: Create a POST endpoint to get questions to play the quiz. This endpoint should 
# take category and previous question parameters and return a random questions 
# within the given category, if provided, and that is not one of the previous questions.
# completed

# TEST: In the "Play" tab, after a user selects "All" or a category, 
# one question at a time is displayed, the user is allowed to answer 
# and shown whether they were correct or not.
#-----------------------------------------------------------------------------------------------!
    @app.route('/quizz', methods=['POST'])
    def play_game():
        # request previous questions list and the quiz category
        get_prev_question_list = request.get_json().get('previous_questions')
        get_quiz_category = request.get_json().get('quiz_category')
        try:
            allCategories = get_category_dict()
            
            # check if the get_quiz_category['id'] exists in the categories or
            # it is not zero i.e. other than zero, or abort(422)
            if int(get_quiz_category['id']) not in allCategories.keys() and int(get_quiz_category['id']) != 0:
                abort(422)
            
            # if the requested quiz category is 0 i.e. ALL the return all the question
            if get_quiz_category['id'] == 0:
                category_questions = Question.query.all()
            else:
                # if not the filter using the requested category_id
                category_questions = Question.query.filter_by(category=get_quiz_category['id']).all()
            
            #empty quiz_questions list to add all the requested category questions
            quiz_questions = []
            
            # get each question item
            for question in category_questions:
                
                # format it
                formatted_question = question.format()
                
                # check if the total category questions is equal to the total previous
                # question list, if yes, return False
                if len(category_questions) == len(get_prev_question_list):
                    return jsonify({
                        'success': False,
                    })
                
                # or else append those questions to the quiz_questions list which are not in the previous questions list
                elif formatted_question['id'] not in get_prev_question_list:
                    quiz_questions.append(formatted_question)

            # get a random question from the quiz question list by generating a random value using random.randint
            #get_random_number = random.randint(0,len(quiz_questions)-1)
            randomized_question = quiz_questions[random.randint(0,len(quiz_questions)-1)]
            return jsonify({
                'success': True,
                'question': randomized_question
            })
        except:
            abort(422)

#-----------------------------------------------------------------------------------------------!
# @TODO: Create error handlers for all expected errors including 404 and 422.
# completed

# Custom request handler for 404 issue
# referenced from https://stackoverflow.com/questions/68399132/failing-to-send-404-http-status-on-flask-when-client-tries-to-get-a-nonexistent
#-----------------------------------------------------------------------------------------------!
    class RequestError(Exception):
        def __init__(self, status):
            self.status = status
        def __str__(self):
            return repr(self.status)
        
# Error Handler for 400  
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400
    
# Error Handler for 404  
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404
        
# Error Handler for 422 
    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable error'
        }), 422

    return app
