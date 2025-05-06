from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# define a function to create a Flask app
def create_app():
    # debug mode is enabled (to be disabled before submission)
    app.debug = True
    # session secret key (to be changed before submission)
    app.secret_key = 'your_secret_key'

    # initialize Flask-Bootstrap
    bootstrap = Bootstrap(app)

    # importing the routes after the app is created to avoid circular imports
    from . import views
    app.register_blueprint(views.bp)
    from . import session
    app.register_blueprint(session.bp)

    return app

@app.errorhandler(404)
# define a custom error handler for 404 errors
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
# define a custom error handler for 500 errors
def page_not_found(e):
    return render_template('500.html'), 500