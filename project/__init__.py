from flask import Flask, render_template, session, Blueprint
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from project.config import Config
import os

mysql = MySQL()
login_manager = LoginManager()

login_manager.login_view = 'main.login'

# define a function to create a Flask app
def create_app():
    # create a Flask app instance
    app = Flask(__name__)

    # MySQL configurations
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # session secret key (to be changed before submission)
    app.secret_key = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # apply config
    app.config.from_object(Config)
    # debug mode is enabled (to be disabled before submission)
    app.debug = True

    # initialize Flask-Bootstrap
    Bootstrap(app)

    # init database & login manager
    mysql.init_app(app)
    login_manager.init_app(app)

    from . import views
    # app.register_blueprint(views.bp)
    app.register_blueprint(views.bp)

    from . import session

    # --- comment database health check ---
    # with app.app_context():
    #     try:
    #         cur = mysql.connection.cursor()
    #         cur.execute("SELECT 1")
    #         cur.close()
    #         print("[DB CHECK] Database is connected.")
    #     except Exception as e:
    #         print(f"[DB CHECK] Error connecting to database: {e}")
    #         raise SystemExit("Exiting due to DB error.")
    #  -------------------------------------

    # add error handler
    @app.errorhandler(404)
    # define a custom error handler for 404 errors
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    # define a custom error handler for 500 errors
    def page_not_found(e):
        return render_template('500.html'), 500

    return app
