from typing import List, Optional, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User, Product, CartItem, Order, Review, Base
from werkzeug.security import generate_password_hash, check_password_hash

# Database setup


class OnlineStore:
    def __init__(self):
        self.products = [] 
        self.carts = {} 
        self.users = []  
        self.next_user_id = 1
        self.next_product_id = 1

    def add_product(self, name, price, description, stock, image_url, category):
        product = {
            'id': self.next_product_id,
            'name': name,
            'price': price,
            'description': description,
            'stock': stock,
            'image_url': image_url,
            'category': category,
            'reviews': [] 
        }
        self.products.append(product)
        self.next_product_id += 1

    def get_all_products(self):
        return self.products

    def get_product_by_id(self, product_id):
        return next((p for p in self.products if p['id'] == product_id), None) 

    def get_cart(self, user_id):
        return self.carts.get(user_id, [])

    def add_to_cart(self, user_id, product_id, quantity=1):
        if user_id not in self.carts:
            self.carts[user_id] = []
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            cart_item = {
                'product_id': product_id,
                'price': product['price'],
                'quantity': quantity
            }
            self.carts[user_id].append(cart_item)

    def remove_from_cart(self, user_id, product_id):
        if user_id in self.carts:
            self.carts[user_id] = [item for item in self.carts[user_id] if item['product_id'] != product_id]

    def clear_cart(self, user_id):
        if user_id in self.carts:
            del self.carts[user_id]

    def add_user(self, email, password, username):
        user_id = len(self.users) + 1
        hashed_password = generate_password_hash(password)
        user = User(user_id, email, hashed_password, username)
        self.users.append(user)

    def add_review(self, product_id, user_id, review_text, username):
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            product['reviews'].append({
                'user_id': user_id,
                'username': username,
                'review_text': review_text
            })

    def get_product_reviews(self, product_id):
        product = next((p for p in self.products if p['id'] == product_id), None)
        return product['reviews'] if product else []

    def register_user(self, username, email, password):
        user_id = len(self.users) + 1
        hashed_password = generate_password_hash(password)
        user = User(user_id, email, hashed_password, username)
        self.users.append(user)
        self.next_user_id += 1
        return user

    def login(self, email: str, password: str) -> Optional[User]:
        for user in self.users:
            if user.email == email and check_password_hash(user.password, password):
                return user
        return None

    def get_product(self, product_id: int) -> Optional[Product]:
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            product['reviews'] = self.get_product_reviews(product['id'])
        return product

    def setup_demo_data(self):
        self.add_product("Gaming Laptop", 1299.99, 
                         "High-performance gaming laptop with Intel Core i7 processor, 16GB RAM, and NVIDIA GeForce GTX 1660 Ti graphics card. Ideal for gaming and graphic work. Equipped with a 15.6-inch display with 1920x1080 resolution and 144Hz refresh rate.", 
                         5, "images/laptop.webp", "Electronics")
        self.add_product("Smartphone", 799.99, 
                         "Latest 5G smartphone with a 6.5-inch AMOLED display, Snapdragon 888 processor, and 128GB storage. Features a triple camera with a 64MP main sensor and supports fast charging.", 
                         15, "images/smartphone.png", "Electronics")
        self.add_product("Wireless Earbuds", 149.99, 
                         "Wireless earbuds with noise cancellation and long battery life. Perfect for listening to music and making calls. Supports Bluetooth 5.0 for stable connectivity.", 
                         30, "images/earbuds.png", "Electronics")
        self.add_product("4K Monitor", 349.99, 
                         "27-inch 4K HDR monitor with excellent color accuracy and high clarity. Ideal for graphic work, gaming, and watching movies. Equipped with multiple ports for connectivity.", 
                         8, "images/monitor.png", "Electronics")
        self.add_product("Backpack", 59.99, 
                         "Waterproof laptop backpack with multiple pockets for organization. Suitable for students and professionals. Features comfortable straps and a stylish design.", 
                         25, "images/backpack.png", "Accessories")
        self.add_product("Mouse", 49.99, 
                         "Wireless gaming mouse with customizable buttons and RGB lighting. Provides high precision and response speed, making it ideal for gamers.", 
                         40, "images/mouse.png", "Accessories")
        self.add_product("Keyboard", 89.99, 
                         "Mechanical keyboard with RGB lighting and tactile feedback. Perfect for gaming and work. Provides comfortable typing and durability.", 
                         20, "images/keyboard.png", "Accessories")
        self.add_product("Webcam", 79.99, 
                         "1080p HD webcam with built-in microphone. Ideal for video calls and streaming. Provides clear image and sound.", 
                         15, "images/webcam.png", "Accessories")
        self.add_product("Smart Watch", 199.99, 
                         "Smartwatch with fitness tracking, heart rate monitoring, and GPS. Ideal for active individuals who want to monitor their health.", 
                         12, "images/smartwatch.png", "Gadgets")
        self.add_product("Tablet", 449.99, 
                         "10-inch tablet with stylus support, perfect for drawing and note-taking. Equipped with a powerful processor and long battery life.", 
                         10, "images/tablet.png", "Gadgets")
        self.add_product("Power Bank", 39.99, 
                         "Portable charger with 20000mAh capacity, capable of charging multiple devices simultaneously. Perfect for travel and active lifestyles.", 
                         50, "images/powerbank.png", "Gadgets")
        self.add_product("Speaker", 129.99, 
                         "Portable Bluetooth speaker with deep bass and long battery life. Ideal for listening to music on the go.", 
                         18, "images/speaker.png", "Gadgets")

    def checkout(self, user_id):
        if user_id in self.carts:

            del self.carts[user_id]
