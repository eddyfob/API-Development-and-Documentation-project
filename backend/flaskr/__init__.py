import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
 
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #Setting up Cross Origin resource sharing
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id:category.type for category in selection}
        #current_questions = paginate_questions(request, selection)
        if len(formatted_categories) == 0:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "categories": formatted_categories,
            }
        )



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=['GET'])
    def retreive_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id:category.type for category in categories}
        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "categories": formatted_categories,
            "current_category": "History",
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question_by_id(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort (404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    # "questions": current_questions,
                    # "total_questions": len(Question.query.all()),
                }
            )
        
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)
        print(search)
        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))).all()
                current_questions = paginate_questions(request, selection)
                category = "Entertainment"
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "current_category": category,
                        "total_questions": len(selection),
                    }
                )

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "total_questions": len(Question.query.all())
                    }
                )
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
   
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:question_category>/questions")
    def get_questions_by_category(question_category):
        categories = Category.query.filter(Category.id == question_category).one_or_none()
        
        if categories is None:
            abort(404)
         
        try:
            questions =  Question.query.filter(Question.category == question_category).all()
            formatted_questions = [question.format() for question in questions]
            
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(questions),
                    "current_category": categories.type
                }
            )
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random question within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer

    and shown whether they were correct or not.
    Endpoint to play game
    """
    @app.route("/quizzes", methods=["POST"])
    def play_game():
        quizzes = request.get_json()
        previous_questions = quizzes.get("previous_questions")
        quiz_category = quizzes.get("quiz_category")["id"]
        try:
            if quiz_category == 0:
                questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
                
            else:
                questions = Question.query.filter(~Question.id.in_(previous_questions)).filter(Question.category == quiz_category).all()
                
            formatted_questions = [question.format() for question in questions]
    
            next_question = random.choice(formatted_questions) if formatted_questions else None
            
            return jsonify({
                "success": True,
                "question": next_question
            })
        except:
            abort(422)  
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "error from server",
            }), 500



    return app

