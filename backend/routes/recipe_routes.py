import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from backend.models.recipe import Recipe
from backend.database import db

recipe_bp = Blueprint('recipes', __name__)

@recipe_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_recipe():
    if 'image' not in request.files:
        return jsonify(message="Image file is required"), 400

    image = request.files['image']
    title = request.form.get('title')
    content = request.form.get('content')
    prep_time = request.form.get('prep_time')
    servings = request.form.get('servings')

    if not title or not content:
        return jsonify(message="Title and content are required"), 400

    if image.filename == '':
        return jsonify(message="No selected file"), 400

    filename = secure_filename(f"{uuid.uuid4().hex}_{image.filename}")
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    image.save(upload_path)

    user_id = int(get_jwt_identity())

    new_recipe = Recipe(
        title=title,
        content=content,
        image_filename=filename,
        user_id=user_id,
        prep_time=prep_time,
        servings=int(servings) if servings else None
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify(message="Recipe uploaded successfully"), 201


@recipe_bp.route('/', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    recipe_list = [
        {
            "id": r.id,
            "title": r.title,
            "image_url": f"/uploads/{r.image_filename}",
            "author": r.user.username
            
        }
        for r in recipes
    ]
    return jsonify(recipe_list), 200


@recipe_bp.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({
        "id": recipe.id,
        "title": recipe.title,
        "content": recipe.content,
        "image_url": f"/uploads/{recipe.image_filename}",
        "prep_time": recipe.prep_time,
        "servings": recipe.servings,
        "author": recipe.user.username
    })
