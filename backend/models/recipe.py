from backend.database import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prep_time = db.Column(db.String(50), nullable=True)
    servings = db.Column(db.Integer, nullable=True)
    user = db.relationship('User', backref='recipes')