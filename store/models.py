from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, user_id, email, password, username):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.username = username
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    stock = Column(Integer)
    image_url = Column(String)
    category = Column(String)

    def __init__(self, id, name, price, description, stock, image_url, category):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
        self.category = category

class CartItem(Base):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, product_id, price, quantity):
        self.product_id = product_id
        self.price = price
        self.quantity = quantity

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)

    def __init__(self, user_id, items, total_amount):
        self.user_id = user_id
        self.items = items  
        self.total_amount = total_amount

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(String)

    def __init__(self, product_id, user_id, review_text):
        self.product_id = product_id
        self.user_id = user_id
        self.review_text = review_text 