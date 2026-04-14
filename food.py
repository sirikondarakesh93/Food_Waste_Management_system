import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect("food.db")
cursor = conn.cursor()

# Create table (with created_time)
cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    food TEXT,
    quantity TEXT,
    location TEXT,
    status TEXT,
    created_time TEXT
)
""")

# Fix old database (add column if missing)
try:
    cursor.execute("ALTER TABLE food ADD COLUMN created_time TEXT")
except:
    pass

conn.commit()


# 🔥 Auto delete expired food (2 hours)
def delete_expired_food():
    expiry_time = (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("DELETE FROM food WHERE created_time < ?", (expiry_time,))
    conn.commit()


# Add food
def add_food():
    name = input("Enter your name: ")
    food = input("Enter food type: ")
    quantity = input("Enter quantity: ")
    location = input("Enter location: ")

    # Validation
    if not name or not food or not quantity or not location:
        print("❌ All fields are required!")
        return

    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO food (name, food, quantity, location, status, created_time) VALUES (?, ?, ?, ?, ?, ?)",
        (name, food, quantity, location, "Available", created_time)
    )
    conn.commit()

    print("\n✅ Food added successfully!\n")


# View food
def view_food():
    delete_expired_food()

    cursor.execute("SELECT * FROM food")
    rows = cursor.fetchall()

    if not rows:
        print("\n❌ No food available\n")
        return

    print("\n📋 Available Food:\n")

    print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
        "ID", "Name", "Food", "Qty", "Location", "Status"
    ))
    print("-" * 75)

    for row in rows:
        print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ))


# Collect food
def collect_food():
    delete_expired_food()

    cursor.execute("SELECT * FROM food WHERE status='Available'")
    rows = cursor.fetchall()

    if not rows:
        print("\n❌ No available food\n")
        return

    print("\n📋 Select Food to Collect:\n")

    print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
        "ID", "Name", "Food", "Qty", "Location", "Status"
    ))
    print("-" * 75)

    for row in rows:
        print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ))

    try:
        food_id = int(input("\nEnter Food ID to collect: "))
    except ValueError:
        print("❌ Enter valid number!")
        return

    cursor.execute("SELECT * FROM food WHERE id=?", (food_id,))
    if not cursor.fetchone():
        print("❌ ID not found!")
        return

    cursor.execute(
        "UPDATE food SET status = ? WHERE id = ?",
        ("Collected", food_id)
    )
    conn.commit()

    print("\n🚚 Food marked as collected!\n")


# Search food
def search_food():
    delete_expired_food()

    print("\n🔍 Search Food")
    print("1. By Location")
    print("2. By Food Type")
    print("3. By Name")

    choice = input("Enter choice: ")

    if choice == '1':
        keyword = input("Enter location: ")
        cursor.execute("SELECT * FROM food WHERE location LIKE ?", ('%' + keyword + '%',))

    elif choice == '2':
        keyword = input("Enter food type: ")
        cursor.execute("SELECT * FROM food WHERE food LIKE ?", ('%' + keyword + '%',))

    elif choice == '3':
        keyword = input("Enter name: ")
        cursor.execute("SELECT * FROM food WHERE name LIKE ?", ('%' + keyword + '%',))

    else:
        print("❌ Invalid choice")
        return

    rows = cursor.fetchall()

    if not rows:
        print("\n❌ No matching records found\n")
        return

    print("\n📋 Search Results:\n")

    print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
        "ID", "Name", "Food", "Qty", "Location", "Status"
    ))
    print("-" * 75)

    for row in rows:
        print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ))


# Near Me Search
def search_near_me():
    delete_expired_food()

    user_location = input("Enter your location: ")

    cursor.execute(
        "SELECT * FROM food WHERE location LIKE ? AND status='Available'",
        ('%' + user_location + '%',)
    )

    rows = cursor.fetchall()

    if not rows:
        print("\n❌ No nearby food found\n")
        return

    print("\n📍 Nearby Available Food:\n")

    print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
        "ID", "Name", "Food", "Qty", "Location", "Status"
    ))
    print("-" * 75)

    for row in rows:
        print("{:<5} {:<15} {:<15} {:<10} {:<15} {:<12}".format(
            row[0], row[1], row[2], row[3], row[4], row[5]
        ))


# Delete all data
def delete_all_data():
    cursor.execute("DELETE FROM food")
    conn.commit()
    print("🗑️ All data deleted!")


# Main menu
def main():
    while True:
        print("\n🍱 Food Donation System")
        print("1. Add Food")
        print("2. View Food")
        print("3. Collect Food")
        print("4. Search Food")
        print("5. Search Near Me")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_food()
        elif choice == '2':
            view_food()
        elif choice == '3':
            collect_food()
        elif choice == '4':
            search_food()
        elif choice == '5':
            search_near_me()
        elif choice == '6':
            confirm = input("Delete all data before exit? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_all_data()
            print("👋 Exiting program...")
            break
        else:
            print("❌ Invalid choice")


# Run program
main()

# Close connection
conn.close()