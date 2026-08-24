import sqlite3

DATABASE = "refind.db"

demo_reports = [
    (
        "Black Leather Wallet",
        "Accessories",
        "Black",
        "Black leather wallet with a small scratch on the front.",
        "Academic Block",
        "Block 3",
        "2026-08-24",
        "11:30",
        "LOST",
        "ACTIVE",
        None
    ),
    (
        "Black Wallet",
        "Accessories",
        "Black",
        "Small black wallet found near the stairs.",
        "Academic Block",
        "Block 3",
        "2026-08-24",
        "11:45",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Blue Water Bottle",
        "Water Bottle",
        "Blue",
        "Blue insulated water bottle with a silver cap.",
        "Library",
        "First Floor",
        "2026-08-24",
        "14:10",
        "LOST",
        "ACTIVE",
        None
    ),
    (
        "Blue Insulated Bottle",
        "Water Bottle",
        "Blue",
        "Blue insulated bottle with silver cap found near a study table.",
        "Library",
        "First Floor",
        "2026-08-24",
        "14:25",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Wireless Earbuds Case",
        "Electronics",
        "White",
        "Small white earbuds charging case.",
        "Cafeteria",
        "Main Area",
        "2026-08-23",
        "13:20",
        "LOST",
        "ACTIVE",
        None
    ),
    (
        "White Earbuds Case",
        "Electronics",
        "White",
        "White wireless earbuds case found under a table.",
        "Cafeteria",
        "Main Area",
        "2026-08-23",
        "13:35",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Student ID Card",
        "ID / Documents",
        "White",
        "College student ID card with a blue border.",
        "Library",
        "Entrance",
        "2026-08-24",
        "09:15",
        "LOST",
        "ACTIVE",
        None
    ),
    (
        "Student ID Card",
        "ID / Documents",
        "White",
        "Student ID card found near the library entrance.",
        "Library",
        "Entrance",
        "2026-08-24",
        "09:25",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Black Backpack",
        "Bags",
        "Black",
        "Black backpack with two front pockets.",
        "Football Field",
        "Side Gate",
        "2026-08-23",
        "17:10",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Red Notebook",
        "Stationery",
        "Red",
        "Red spiral notebook with handwritten notes.",
        "Academic Block",
        "Block 2",
        "2026-08-22",
        "10:40",
        "LOST",
        "ACTIVE",
        None
    ),
    (
        "Silver Laptop Charger",
        "Electronics",
        "Silver",
        "Laptop charger with a black cable.",
        "Administrative Block",
        "Room 204",
        "2026-08-23",
        "15:30",
        "FOUND",
        "ACTIVE",
        None
    ),
    (
        "Grey Hoodie",
        "Clothing",
        "Grey",
        "Grey hoodie with a small logo on the chest.",
        "Gym",
        "Changing Room",
        "2026-08-24",
        "18:00",
        "LOST",
        "ACTIVE",
        None
    )
]


connection = sqlite3.connect(DATABASE)

connection.execute("PRAGMA foreign_keys = ON")

for report in demo_reports:

    connection.execute(
        """
        INSERT INTO reports (
            item_name,
            category,
            color,
            description,
            location_type,
            location_details,
            date_lost,
            time_lost,
            report_type,
            status,
            image_filename
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        report
    )

connection.commit()
connection.close()

print("Demo reports added successfully.")