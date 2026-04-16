from flask import Flask, jsonify, request, send_from_directory
import os
from flask_cors import CORS

from .extensions import db, migrate, jwt, mail
from .config import Config

# Import route blueprints
from .routes.users_route import users_bp
from .routes.projects_route import projects_bp
from .routes.skills_route import skills_bp
from .routes.experience_route import experience_bp
from .routes.education_route import education_bp
from .routes.contact_route import contact_bp
from .routes.blog_route import blog_bp
from .routes.portfolio_route import portfolio_bp
from .routes.images_route import images_bp
from sqlalchemy import inspect

# Standalone backend app. Frontend is deployed separately.
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
mail.init_app(app)

# Allow only configured frontend origins in production.
CORS(
    app,
    resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    supports_credentials=True,
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials",
        "Accept",
        "Origin",
        "X-Requested-With",
    ],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    expose_headers=["Content-Range", "X-Content-Range"],
)

@app.after_request
def after_request(response):
    allowed_origins = app.config["CORS_ORIGINS"]
    request_origin = request.headers.get("Origin")
    if "*" in allowed_origins and request_origin:
        response.headers["Access-Control-Allow-Origin"] = request_origin
    elif "*" in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif request_origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = request_origin

    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type,Authorization,Accept,Origin,X-Requested-With"
    )
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS,PATCH"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# NOTE: Avoid db.create_all() on import/startup.
# Flask-Migrate/Alembic should own schema creation via migrations; calling create_all
# causes "DuplicateTable" errors when migrations run against a fresh database.

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/api/auth')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(skills_bp, url_prefix='/api')
app.register_blueprint(experience_bp, url_prefix='/api')
app.register_blueprint(education_bp, url_prefix='/api')
app.register_blueprint(contact_bp, url_prefix='/api')
app.register_blueprint(blog_bp, url_prefix='/api')
app.register_blueprint(portfolio_bp, url_prefix='/api')
app.register_blueprint(images_bp, url_prefix='/api/images')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403

@app.route("/")
def index():
    return jsonify({
        "service": "portfolio-backend",
        "status": "ok",
        "docs": "Use /api/* endpoints",
    })

# Serve static files (uploads)
@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory('static/uploads', filename)    

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    })

# DB diagnostics endpoint (read-only)
@app.route('/debug/db')
def debug_db():
    try:
        uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        # For sqlite path extraction
        sqlite_path = None
        if uri and uri.startswith('sqlite:///'):
            sqlite_path = uri.replace('sqlite:///', '').split('?', 1)[0]
        exists = None
        if sqlite_path:
            exists = os.path.exists(sqlite_path)
        return jsonify({
            "database_uri": uri,
            "sqlite_path": sqlite_path,
            "sqlite_file_exists": exists,
            "tables": tables,
            "has_education_table": 'education' in tables,
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')