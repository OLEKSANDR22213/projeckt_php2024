from flask import Flask, render_template, request, redirect, url_for, flash, session
from store.store import OnlineStore
from store.models import User, Product, CartItem, Order, Review, Base
from store.payment import PaymentProcessor
from store.models import CartItem 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '13jfnfFGIUJonGiugjhG80hjgGH8'
store = OnlineStore()
store.setup_demo_data() 


# Setup some demo data
def setup_demo_data():
    # Electronics
    store.add_product("Gaming Laptop", 1299.99, "High-performance gaming laptop", 5, "images/laptop.webp", "Electronics")
    store.add_product("Smartphone", 799.99, "Latest 5G smartphone", 15, "images/smartphone.png", "Electronics")
    store.add_product("Wireless Earbuds", 149.99, 
                      "Noise-cancelling bluetooth earbuds with long battery life and superior sound quality.", 
                      30, "images/earbuds.png", "Electronics")
    store.add_product("4K Monitor", 349.99, 
                      "27-inch 4K HDR display with vibrant colors and ultra-smooth performance.", 
                      8, "images/monitor.png", "Electronics")
    
    # Accessories
    store.add_product("Backpack", 59.99, 
                        "Water-resistant laptop backpack with multiple compartments for organization.", 
                      25, "images/backpack.png", "Accessories")
    store.add_product("Mouse", 49.99, 
                      "Wireless gaming mouse with customizable buttons and RGB lighting.", 
                      40, "images/mouse.png", "Accessories")
    store.add_product("Keyboard", 89.99, 
                      "Mechanical RGB keyboard with tactile feedback and customizable lighting.", 
                      20, "images/keyboard.png", "Accessories")
    store.add_product("Webcam", 79.99, 
                      "1080p HD webcam with microphone, ideal for video conferencing and streaming.", 
                      15, "images/webcam.png", "Accessories")
    
    # Gadgets
    store.add_product("Smart Watch", 199.99, 
                      "Fitness tracking smartwatch with heart rate monitor and GPS.", 
                      12, "images/smartwatch.png", "Gadgets")
    store.add_product("Tablet", 449.99, 
                      "10-inch tablet with stylus support, perfect for drawing and note-taking.", 
                      10, "images/tablet.png", "Gadgets")
    store.add_product("Power Bank", 39.99, 
                      "20000mAh portable charger, capable of charging multiple devices.", 
                      50, "images/powerbank.png", "Gadgets")
    store.add_product("Speaker", 129.99, 
                      "Portable bluetooth speaker with deep bass and long battery life.", 
                      18, "images/speaker.png", "Gadgets")

@app.route('/')
def home():
    products = store.get_all_products()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = next((u for u in store.users if u.email == email), None)
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['email'] = email
            session['username'] = user.username  # Сохраняем имя пользователя
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        store.register_user(username, email, password)  # Передаем правильные аргументы
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = store.get_cart(session['user_id'])
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

    # Передаем объект store в шаблон
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount, store=store)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    store.add_to_cart(session['user_id'], product_id, quantity=1)  # Добавляем продукт в корзину
    flash('Product added to cart!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET'])
def checkout_page():
    if 'user_id' not in session:
        flash('You must be logged in to checkout.', 'error')
        return redirect(url_for('login'))
    
    cart_items = store.get_cart(session['user_id'])
    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    if 'user_id' not in session:
        flash('You must be logged in to checkout.', 'error')
        return redirect(url_for('login'))
    
    # Логика обработки заказа
    store.checkout(session['user_id'])
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('order_successful'))

@app.route('/order_successful', methods=['GET'])
def order_successful():
    return render_template('order_success.html')

@app.route('/another_order_successful', methods=['GET'])
def another_order_successful():
    return render_template('another_order_successful.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in store.products if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('home'))
    return render_template('product_detail.html', product=product)

@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):
    if 'user_id' not in session:
        flash('You must be logged in to leave a review.', 'error')
        return redirect(url_for('login'))
    
    review_text = request.form['review']
    user_id = session['user_id']
    username = session.get('username')  # Используем get для безопасного извлечения
    store.add_review(product_id, user_id, review_text, username)
    flash('Your review has been submitted!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        flash('You must be logged in to remove items from your cart.', 'error')
        return redirect(url_for('login'))
    
    store.remove_from_cart(session['user_id'], product_id)  # Удаляем товар из корзины
    flash('Item removed from cart!', 'success')
    return redirect(url_for('cart'))  # Перенаправляем на страницу корзины

@app.route('/submit_product', methods=['POST'])
def submit_product():
    product_name = request.form['product_name']
    price = request.form['price']
    description = request.form['description']
    
    # Логика добавления продукта
    store.add_product(product_name, price, description)
    flash('Product submitted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)