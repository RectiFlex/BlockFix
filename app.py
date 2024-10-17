import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Generate a strong secret key if not provided
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['INVENTORY_API_URL'] = os.environ.get('INVENTORY_API_URL', 'https://api.example.com/v1')
app.config['INVENTORY_API_KEY'] = os.environ.get('INVENTORY_API_KEY', 'your-api-key')

# Ensure debug mode is off in production
app.config['DEBUG'] = False

# Configure SSL/TLS (if using a reverse proxy like Nginx, this can be handled there)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True

db.init_app(app)
migrate = Migrate(app, db)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore

# Set up CSRF protection
csrf = CSRFProtect(app)

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Set up logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/rectiflex.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Rectiflex startup')

# Error handling for production
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

from routes import *
from external_systems import init_inventory_system

with app.app_context():
    init_inventory_system(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), use_reloader=False, log_output=True)
