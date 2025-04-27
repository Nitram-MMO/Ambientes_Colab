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
    
def register_user():
    users = load_json(USER_FILE)
    username = input("Enter new username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input("Enter new password: ")
    users[username] = {"password": password}
    save_json(USER_FILE, users)
    print("Account created successfully!")
    
def login_user():
    users = load_json(USER_FILE)
    username = input("Username: ")
    password = input("Password: ")
    if username == "manager" and password == "manager":
        print("Logged in as Manager!")
        return "manager"
    if username in users and users[username]["password"] == password:
        print(f"Welcome {username}!")
        return username
    else:
        print("Invalid credentials.")
        return None
    
def generate_weekly_menu():
    menu = {}
    for week in range(1, 5):
        week_menu = {}
        meat_choices = random.sample(meat_dishes, len(DAYS))
        fish_choices = random.sample(fish_dishes, len(DAYS))
        vegetarian_choices = random.sample(vegetarian_dishes, len(DAYS))
        for i, day in enumerate(DAYS):
            week_menu[day] = {
                "Meat": {"dish": meat_choices[i], "price": FIXED_PRICE},
                "Fish": {"dish": fish_choices[i], "price": FIXED_PRICE},
                "Vegetarian": {"dish": vegetarian_choices[i], "price": FIXED_PRICE}
            }
        menu[f"Week{week}"] = week_menu
    save_json(MENU_FILE, menu)
    
def view_weekly_menu():
    menu = load_json(MENU_FILE)
    week_number = input("Enter week number (1-4): ")
    week_key = f"Week{week_number}"
    if week_key not in menu:
        print("No menu available for that week.")
        return
    week_menu = menu[week_key]
    for day, dishes in week_menu.items():
        print(f"\n{day}:")
        for category, item in dishes.items():
            print(f"  {category}: {item['dish']} - {item['price']}€")
            

def edit_weekly_menu():
    menu = load_json(MENU_FILE)
    week_number = input("Enter week number to edit (1-4): ")
    week_key = f"Week{week_number}"
    if week_key not in menu:
        print("No menu for that week.")
        return

    day = None
    while day is None:
        day_input = input("Enter day to edit (Monday-Friday): ")
        day = normalize_day(day_input)

    if day not in menu[week_key]:
        print("Invalid day.")
        return

    print("\nCurrent dishes:")
    for category, item in menu[week_key][day].items():
        print(f"{category}: {item['dish']} - {item['price']}€")
    
    category = input("Enter category to edit (Meat/Fish/Vegetarian): ").capitalize()
    if category not in ["Meat", "Fish", "Vegetarian"]:
        print("Invalid category.")
        return

    new_dish = input(f"Enter new dish name for {category}: ")
    menu[week_key][day][category]["dish"] = new_dish
    save_json(MENU_FILE, menu)
    print("Dish updated successfully!")

def order_dish(username):
    menu = load_json(MENU_FILE)
    week_number = input("Enter current week number (1-4): ")
    week_key = f"Week{week_number}"
    if week_key not in menu:
        print("No menu available for that week.")
        return

    day = None
    while day is None:
        day_input = input("Enter today (Monday-Friday): ")
        day = normalize_day(day_input)

    if day not in menu[week_key]:
        print("Invalid day.")
        return

    print("\nAvailable dishes:")
    dishes = menu[week_key][day]
    for idx, (category, item) in enumerate(dishes.items(), 1):
        print(f"{idx}. {category}: {item['dish']} - {item['price']}€")

    choice = input("Choose a dish number to save: ")
    try:
        choice = int(choice)
        if 1 <= choice <= 3:
            category = list(dishes.keys())[choice-1]
            selected_dish = dishes[category]["dish"]
            orders = load_json(ORDERS_FILE)
            if username not in orders:
                orders[username] = []
            orders[username].append({"week": week_number, "day": day, "dish": selected_dish})
            save_json(ORDERS_FILE, orders)
            print(f"Dish {selected_dish} saved successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")
        
def delete_saved_dish(username):
    orders = load_json(ORDERS_FILE)
    if username not in orders or not orders[username]:
        print("No saved orders.")
        return
    
    print("\nYour saved dishes:")
    for idx, order in enumerate(orders[username], 1):
        print(f"{idx}. Week {order['week']} - {order['day']}: {order['dish']}")

    choice = input("Enter the number of the dish you want to delete: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(orders[username]):
            deleted_dish = orders[username].pop(choice - 1)
            save_json(ORDERS_FILE, orders)
            print(f"Dish {deleted_dish['dish']} deleted successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")
        
def view_saved_orders(username):
    orders = load_json(ORDERS_FILE)
    if username not in orders or not orders[username]:
        print("No saved orders.")
        return
    print("\nYour saved dishes:")
    for order in orders[username]:
        print(f"Week {order['week']} - {order['day']}: {order['dish']}")