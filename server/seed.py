#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Clear existing data to avoid duplicates
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Create Restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Main St")
    bistro = Restaurant(name="Sanjay's Pizza", address="456 Elm St")
    palace = Restaurant(name="Kiki's Pizza", address="789 Oak St")
    restaurants = [shack, bistro, palace]

    # Add Restaurants to the session
    db.session.add_all(restaurants)
    db.session.commit()

    # Create Pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    # Add Pizzas to the session
    db.session.add_all(pizzas)
    db.session.commit()

    # Create RestaurantPizza entries
    print("Creating restaurant_pizzas...")
    rp1 = RestaurantPizza(restaurant_id=shack.id, pizza_id=cheese.id, price=10)
    rp2 = RestaurantPizza(restaurant_id=bistro.id, pizza_id=pepperoni.id, price=15)
    rp3 = RestaurantPizza(restaurant_id=palace.id, pizza_id=california.id, price=20)
    restaurant_pizzas = [rp1, rp2, rp3]

    # Add RestaurantPizza to the session
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")
