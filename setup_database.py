# setup_database.py

import sqlite3

# --- DATABASE SETUP ---
DATABASE = 'ecommerce.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

# --- DROP EXISTING TABLES (for a clean slate) ---
print("Dropping old tables...")
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS products")
c.execute("DROP TABLE IF EXISTS orders")
c.execute("DROP TABLE IF EXISTS order_items")
c.execute("DROP TABLE IF EXISTS inventory_items")
c.execute("DROP TABLE IF EXISTS distribution_centers")

# --- CREATE TABLES ---
print("Creating new tables...")

# Users Table
c.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Products Table
c.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL
)
""")

# Distribution Centers Table
c.execute("""
CREATE TABLE distribution_centers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL
)
""")

# Orders Table
c.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    order_date DATE NOT NULL,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

# Order Items Table (Junction table)
c.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

# Inventory Items Table
c.execute("""
CREATE TABLE inventory_items (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    distribution_center_id INTEGER,
    stock_level INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(product_id),
    FOREIGN KEY(distribution_center_id) REFERENCES distribution_centers(id)
)
""")


# --- INSERT SAMPLE DATA ---
print("Inserting sample data...")

# Sample Data
users_data = [
    ('John', 'Doe', 'john.doe@example.com'),
    ('Jane', 'Smith', 'jane.smith@example.com'),
    ('Peter', 'Jones', 'peter.jones@email.com')
]

products_data = [
    ('Laptop', 'Electronics', 1200.00),
    ('Mouse', 'Electronics', 25.00),
    ('Keyboard', 'Electronics', 75.00),
    ('Desk Chair', 'Furniture', 150.00)
]

distribution_centers_data = [
    ('DC East', 'New York, NY'),
    ('DC West', 'Los Angeles, CA'),
    ('DC Central', 'Chicago, IL')
]

orders_data = [
    (1, '2023-10-01', 'Shipped'),
    (2, '2023-10-03', 'Processing'),
    (1, '2023-11-05', 'Delivered') # A second order for John Doe
]

order_items_data = [
    (1, 1, 1), # Order 1, Product 1 (Laptop), Quantity 1
    (1, 2, 2), # Order 1, Product 2 (Mouse), Quantity 2
    (2, 4, 1), # Order 2, Product 4 (Desk Chair), Quantity 1
    (3, 3, 1)  # Order 3, Product 3 (Keyboard), Quantity 1
]

inventory_items_data = [
    (1, 1, 100), # Product 1 (Laptop) at DC East has 100 stock
    (2, 1, 250), # Product 2 (Mouse) at DC East has 250 stock
    (3, 2, 300), # Product 3 (Keyboard) at DC West has 300 stock
    (4, 3, 50)   # Product 4 (Desk Chair) at DC Central has 50 stock
]

# Execute inserts
c.executemany("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)", users_data)
c.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products_data)
c.executemany("INSERT INTO distribution_centers (name, location) VALUES (?, ?)", distribution_centers_data)
c.executemany("INSERT INTO orders (user_id, order_date, status) VALUES (?, ?, ?)", orders_data)
c.executemany("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", order_items_data)
c.executemany("INSERT INTO inventory_items (product_id, distribution_center_id, stock_level) VALUES (?, ?, ?)", inventory_items_data)

# --- COMMIT AND CLOSE ---
conn.commit()
conn.close()

print("Database 'ecommerce.db' created and populated successfully!")