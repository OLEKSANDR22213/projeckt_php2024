from dataclasses import dataclass, field
from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User:
    def __init__(self, user_id, email, password, username):
        self.id = user_id
        self.email = email
        self.password = password
        self.username = username

class Product:
    def __init__(self, product_id, name, price, description, stock, image_url, category):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.image_url = image_url
        self.category = category
        self.reviews = []  # List to store reviews

class Review:
    def __init__(self, user, product, text):
        self.user = user
        self.product = product
        self.text = text

@dataclass
class CartItem:
    product: Product
    quantity: int

@dataclass
class Order:
    id: int
    user_id: int
    items: List[CartItem]
    status: str 
