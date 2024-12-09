from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_cream_parlor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Models for the database
class SeasonalFlavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(100), nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flavor_id = db.Column(db.Integer, db.ForeignKey('seasonal_flavor.id'), nullable=False)
    seasonal_flavor = db.relationship('SeasonalFlavor', back_populates="ingredients")

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor_suggestion = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.String(100), nullable=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor_id = db.Column(db.Integer, db.ForeignKey('seasonal_flavor.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    seasonal_flavor = db.relationship('SeasonalFlavor', back_populates="cart_items")


SeasonalFlavor.ingredients = db.relationship('Ingredient', back_populates="seasonal_flavor")
SeasonalFlavor.cart_items = db.relationship('Cart', back_populates="seasonal_flavor")


# Initialize the database (only need to do once)
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return 'Welcome to the Ice Cream Parlor!'


# Route to manage seasonal flavors (GET and POST)
@app.route('/flavors', methods=['GET', 'POST'])
def manage_flavors():
    if request.method == 'GET':
        flavors = SeasonalFlavor.query.all()
        return jsonify([{'id': f.id, 'name': f.name, 'season': f.season} for f in flavors])

    if request.method == 'POST':
        data = request.get_json()
        new_flavor = SeasonalFlavor(name=data['name'], season=data['season'])
        db.session.add(new_flavor)
        db.session.commit()
        return jsonify({'id': new_flavor.id, 'name': new_flavor.name, 'season': new_flavor.season}), 201


# Route to manage ingredients (GET and POST)
@app.route('/ingredients', methods=['GET', 'POST'])
def manage_ingredients():
    if request.method == 'GET':
        ingredients = Ingredient.query.all()
        return jsonify([{'id': i.id, 'name': i.name, 'flavor_id': i.flavor_id} for i in ingredients])

    if request.method == 'POST':
        data = request.get_json()
        new_ingredient = Ingredient(name=data['name'], flavor_id=data['flavor_id'])
        db.session.add(new_ingredient)
        db.session.commit()
        return jsonify({'id': new_ingredient.id, 'name': new_ingredient.name, 'flavor_id': new_ingredient.flavor_id}), 201


# Route to handle customer flavor suggestions and allergies (GET and POST)
@app.route('/suggestions', methods=['GET', 'POST'])
def manage_suggestions():
    if request.method == 'GET':
        suggestions = Suggestion.query.all()
        return jsonify([{'id': s.id, 'flavor_suggestion': s.flavor_suggestion, 'allergies': s.allergies} for s in suggestions])

    if request.method == 'POST':
        data = request.get_json()
        new_suggestion = Suggestion(flavor_suggestion=data['flavor_suggestion'], allergies=data['allergies'])
        db.session.add(new_suggestion)
        db.session.commit()
        return jsonify({'id': new_suggestion.id, 'flavor_suggestion': new_suggestion.flavor_suggestion, 'allergies': new_suggestion.allergies}), 201


# Route to handle allergens (GET and POST)
@app.route('/allergens', methods=['GET', 'POST'])
def manage_allergens():
    if request.method == 'GET':
        allergens = db.session.query(Suggestion).filter(Suggestion.allergies.isnot(None)).all()
        return jsonify([{'id': s.id, 'flavor_suggestion': s.flavor_suggestion, 'allergies': s.allergies} for s in allergens])

    if request.method == 'POST':
        data = request.get_json()
        new_allergen = Suggestion(flavor_suggestion=data['flavor_suggestion'], allergies=data['allergies'])
        db.session.add(new_allergen)
        db.session.commit()
        return jsonify({'id': new_allergen.id, 'flavor_suggestion': new_allergen.flavor_suggestion, 'allergies': new_allergen.allergies}), 201


# Route to manage the cart (GET and POST)
@app.route('/cart', methods=['GET', 'POST'])
def manage_cart():
    if request.method == 'GET':
        cart_items = Cart.query.all()
        return jsonify([{'id': c.id, 'flavor_id': c.flavor_id, 'quantity': c.quantity} for c in cart_items])

    if request.method == 'POST':
        data = request.get_json()
        new_cart_item = Cart(flavor_id=data['flavor_id'], quantity=data['quantity'])
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({'id': new_cart_item.id, 'flavor_id': new_cart_item.flavor_id, 'quantity': new_cart_item.quantity}), 201


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
