#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
import os

# Setup database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize database and migrations
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful
api = Api(app)


# Resource: Restaurants
class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in restaurants], 200


class RestaurantByIdResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(rules=("-restaurant_pizzas.pizza",)), 200

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204


# Resource: Pizzas
class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in pizzas], 200


# Resource: RestaurantPizzas
class RestaurantPizzasResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            price = data.get("price")
            pizza_id = data.get("pizza_id")
            restaurant_id = data.get("restaurant_id")

            # Validate price
            if price is None or not (1 <= price <= 30):
                return {"errors": ["Price must be between 1 and 30."]}, 400

            # Check for associated Pizza and Restaurant
            pizza = Pizza.query.filter_by(id=pizza_id).first()
            restaurant = Restaurant.query.filter_by(id=restaurant_id).first()

            if not pizza or not restaurant:
                return {"errors": ["Invalid pizza_id or restaurant_id"]}, 400

            # Create new RestaurantPizza
            restaurant_pizza = RestaurantPizza(
                price=price, pizza_id=pizza_id, restaurant_id=restaurant_id
            )
            db.session.add(restaurant_pizza)
            db.session.commit()

            return restaurant_pizza.to_dict(rules=("pizza", "restaurant")), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400


# Register routes
api.add_resource(RestaurantsResource, "/restaurants")
api.add_resource(RestaurantByIdResource, "/restaurants/<int:id>")
api.add_resource(PizzasResource, "/pizzas")
api.add_resource(RestaurantPizzasResource, "/restaurant_pizzas")


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
