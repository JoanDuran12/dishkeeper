from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.config import Config
from backend.database import db

from backend.routes.auth_routes import auth_bp
from backend.routes.recipe_routes import recipe_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)
db.init_app(app)

jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(recipe_bp, url_prefix="/api/recipes")

from flask import send_from_directory

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
