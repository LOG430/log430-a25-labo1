"""
Product model
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

class Product:
    def __init__(self, id=None, name=None, brand=None, price=None):
        self.id = id
        self.name = name
        self.brand = brand
        self.price = price
    
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', brand='{self.brand}', price={self.price})"