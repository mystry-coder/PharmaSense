"""
init_db.py
-----------
This script creates a small SQLite database (pharmasense.db) filled with
FAKE / SYNTHETIC pharma sales data — sales reps, doctors (HCPs = Health
Care Professionals), territories, and sales transactions.

Why SQLite? It's just a single file, no server to install, and Python has
built-in support for it (the `sqlite3` module). Perfect for a quick project.

Run this once with:
    python init_db.py

It will create/overwrite pharmasense.db in the same folder.
"""

import sqlite3
import random
from datetime import date, timedelta

# ---- 1. Connect to (or create) the database file ----
conn = sqlite3.connect("pharmasense.db")
cur = conn.cursor()

# ---- 2. Drop old tables if they exist (so we can re-run this safely) ----
cur.executescript("""
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS reps;
DROP TABLE IF EXISTS hcps;
DROP TABLE IF EXISTS territories;
DROP TABLE IF EXISTS products;
""")

# ---- 3. Create tables ----
cur.executescript("""
CREATE TABLE territories (
    territory_id INTEGER PRIMARY KEY,
    territory_name TEXT NOT NULL
);

CREATE TABLE reps (
    rep_id INTEGER PRIMARY KEY,
    rep_name TEXT NOT NULL,
    territory_id INTEGER,
    FOREIGN KEY (territory_id) REFERENCES territories(territory_id)
);

CREATE TABLE hcps (
    hcp_id INTEGER PRIMARY KEY,
    hcp_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    territory_id INTEGER,
    FOREIGN KEY (territory_id) REFERENCES territories(territory_id)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    rep_id INTEGER,
    hcp_id INTEGER,
    product_id INTEGER,
    sale_date TEXT,
    units_sold INTEGER,
    revenue REAL,
    FOREIGN KEY (rep_id) REFERENCES reps(rep_id),
    FOREIGN KEY (hcp_id) REFERENCES hcps(hcp_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# ---- 4. Insert reference data ----
territories = ["North", "South", "East", "West", "Central"]
for i, t in enumerate(territories, start=1):
    cur.execute("INSERT INTO territories VALUES (?, ?)", (i, t))

rep_names = ["Ananya Roy", "Vikram Shah", "Priya Nair", "Rohan Mehta",
             "Sneha Iyer", "Arjun Das", "Kavya Reddy", "Aditya Kapoor"]
for i, name in enumerate(rep_names, start=1):
    cur.execute("INSERT INTO reps VALUES (?, ?, ?)",
                (i, name, random.randint(1, len(territories))))

specialties = ["Cardiology", "Oncology", "Endocrinology", "Neurology", "Pediatrics"]
hcp_names = [f"Dr. {n}" for n in
             ["Sharma", "Gupta", "Banerjee", "Iyer", "Khan", "Verma",
              "Chatterjee", "Pillai", "Joshi", "Mukherjee", "Rao", "Singh"]]
for i, name in enumerate(hcp_names, start=1):
    cur.execute("INSERT INTO hcps VALUES (?, ?, ?, ?)",
                (i, name, random.choice(specialties), random.randint(1, len(territories))))

products = [
    ("CardioEase", "Cardiology"),
    ("OncoRelief", "Oncology"),
    ("GlucoBalance", "Endocrinology"),
    ("NeuroCalm", "Neurology"),
    ("PediaSafe", "Pediatrics"),
]
for i, (name, cat) in enumerate(products, start=1):
    cur.execute("INSERT INTO products VALUES (?, ?, ?)", (i, name, cat))

# ---- 5. Generate random sales transactions over the last 6 months ----
start_date = date.today() - timedelta(days=180)
sale_id = 1
for _ in range(500):
    rep_id = random.randint(1, len(rep_names))
    hcp_id = random.randint(1, len(hcp_names))
    product_id = random.randint(1, len(products))
    sale_date = start_date + timedelta(days=random.randint(0, 180))
    units = random.randint(1, 50)
    price_per_unit = round(random.uniform(200, 1500), 2)
    revenue = round(units * price_per_unit, 2)

    cur.execute(
        "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sale_id, rep_id, hcp_id, product_id, sale_date.isoformat(), units, revenue)
    )
    sale_id += 1

# ---- 6. Save and close ----
conn.commit()
conn.close()

print("✅ pharmasense.db created with synthetic data.")
print("Tables: territories, reps, hcps, products, sales (500 sales records)")
