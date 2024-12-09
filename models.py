# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SeasonalFlavor(db.Model):
    __tablename__ = 'seasonal_flavors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    season = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<SeasonalFlavor {self.name}>"

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}>"

class CustomerSuggestion(db.Model):
    __tablename__ = 'customer_suggestions'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(100), nullable=False)
    suggestion = db.Column(db.Text, nullable=False)
    allergy_concerns = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<CustomerSuggestion {self.flavor}>"

class Allergen(db.Model):
    __tablename__ = 'allergens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Allergen {self.name}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    flavor_id = db.Column(db.Integer, db.ForeignKey('seasonal_flavors.id'), nullable=False)
    user = db.Column(db.String(100), nullable=False)

    flavor = db.relationship('SeasonalFlavor')

    def __repr__(self):
        return f"<CartItem {self.flavor.name} for {self.user}>"
