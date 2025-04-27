import os
import json
import random


#constants to be used 

USER_FILE = "user.json"
MENU_FILE = "menu.json"
ORDERS_FILE = "orders.json"
FIXED_PRICE = 2.80

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

meat_dishes = ["Steak", "Chicken Curry", "Pork Chops", "Beef Stew", "Grilled Lamb"]
fish_dishes = ["Grilled Salmon", "Fish and Chips", "Tuna Salad", "Shrimp Pasta", "Baked Cod"]
vegetarian_dishes = ["Veggie Burger", "Pasta Primavera", "Grilled Vegetables", "Tofu Stir-fry", "Vegetable Curry"]

def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
def normalize_day(day_input):
    day_input = day_input.strip().lower().capitalize()
    if day_input in DAYS:
        return day_input
    else:
        print("Invalid day entered. Please try again.")
        return None