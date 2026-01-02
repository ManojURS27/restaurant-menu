from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'restaurant_secret_key'

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

menu_data = {
    "Starters": [
        MenuItem("Gobi Manchurian", 130.00 ),
        MenuItem("Mushroom Manchurian", 150.00 ),
        MenuItem("Paneer Manchurian", 150.00),
        MenuItem("Baby Corn Manchurian", 140.00)
    ],
    "Soups": [
        MenuItem("Hot and Sour", 200.00),
        MenuItem("Manchow Soup", 150.00),
        MenuItem("Garlic Soup", 180.00 ),
        MenuItem ("Tomato Soup",150.00)
    ],
    "Main Course": [
        MenuItem("Veg biryani", 120.00),
        MenuItem("Paneer biryani", 140.00),
        MenuItem("Mushroom biryani", 140.00),
        MenuItem("Ghee Rice", 100.00),
        MenuItem("Jeera Rice", 100.00),
        MenuItem("White Rice", 80.00),
        MenuItem("Curd Rice", 100.00)    ],
    "Juice/Shakes": [
        MenuItem("Lemon Soda", 60.00),
        MenuItem("Dry Fruit Shake", 120.00),
        MenuItem("Banana Shake", 80.00),
        MenuItem("Litchi Shake", 120.00),
        MenuItem("Double Sundae", 100.00),
        MenuItem("Gud Bud Ice Cream", 140.00)
    ]
}

def get_item_price(name):
    for category in menu_data.values():
        for item in category:
            if item.name == name:
                return item.price
    return 0.0

@app.route('/')
def index():
    if 'cart' not in session:
        session['cart'] = {}
    
    total = sum(item['price'] * item['quantity'] for item in session['cart'].values())
    return render_template('index.html', menu=menu_data, cart=session['cart'], total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    name = request.form.get('name')
    qty = int(request.form.get('quantity', 1))
    
    # Securely get price from our menu_data, not the user's form
    price = get_item_price(name)
    
    cart = session.get('cart', {})
    if name in cart:
        cart[name]['quantity'] += qty
    else:
        cart[name] = {'price': price, 'quantity': qty}
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('index'))

@app.route('/remove/<name>')
def remove_item(name):
    cart = session.get('cart', {})
    if name in cart:
        del cart[name]
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('index'))

@app.route('/clear')
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(debug=True)
