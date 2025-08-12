# app.py

from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'ecommerce.db'  # your SQLite database file

def query_db(query, args=(), one=False):
    """A utility function to query the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # access columns by name
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# API: Search users by first_name, last_name or email (case-insensitive)
@app.route('/api/users', methods=['GET'])
def get_users():
    search_term = request.args.get('search', '').lower().strip()
    if search_term:
        like_term = f'%{search_term}%'
        rows = query_db(
            """
            SELECT * FROM users 
            WHERE LOWER(first_name) LIKE ? 
               OR LOWER(last_name) LIKE ? 
               OR LOWER(email) LIKE ?
            ORDER BY first_name, last_name
            """,
            (like_term, like_term, like_term)
        )
    else:
        rows = query_db("SELECT * FROM users ORDER BY first_name, last_name")
    return jsonify([dict(row) for row in rows])

# API: Get orders for a specific user_id
@app.route('/api/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    rows = query_db("SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC", (user_id,))
    return jsonify([dict(row) for row in rows])

# API: Get items for a specific order_id, including product details
@app.route('/api/orders/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    rows = query_db("""
        SELECT 
            oi.quantity,
            p.name,
            p.category,
            p.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    """, (order_id,))
    return jsonify([dict(row) for row in rows])

# API: Get all inventory items
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    rows = query_db("""
        SELECT 
            p.name as product_name,
            dc.name as distribution_center,
            ii.stock_level
        FROM inventory_items ii
        JOIN products p ON ii.product_id = p.product_id
        JOIN distribution_centers dc ON ii.distribution_center_id = dc.id
        ORDER BY p.name
    """)
    return jsonify([dict(row) for row in rows])

# API: Get all distribution centers
@app.route('/api/distribution', methods=['GET'])
def get_distribution_centers():
    rows = query_db("SELECT name, location FROM distribution_centers ORDER BY name")
    return jsonify([dict(row) for row in rows])

# Frontend route serving index.html
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)