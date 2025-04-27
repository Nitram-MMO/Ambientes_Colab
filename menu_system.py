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
    
def main():
    if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
        generate_weekly_menu()

    while True:
        print("\n1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user = login_user()
            if user:
                if user == "manager":
                    manager_menu()
                else:
                    while True:
                        print("\nStudent Menu")
                        print("1. View Weekly Menu")
                        print("2. Save Dish for Today")
                        print("3. View Saved Dishes")
                        print("4. Delete saved orders")
                        print("5. Logout")
                        student_choice = input("Choose an option: ")
                        if student_choice == "1":
                            view_weekly_menu()
                        elif student_choice == "2":
                            order_dish(user)
                        elif student_choice == "3":
                            view_saved_orders(user)
                        elif student_choice == "4":
                            delete_saved_dish(user)
                        elif student_choice == "5":
                            break
                        else:
                            print("Invalid option.")
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")