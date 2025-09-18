"""
Product controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from daos.product_dao import ProductDAO

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

    def list_products(self):
        """ List all products """
        return self.dao.select_all()

    def create_product(self, product):
        """ Create a new product based on product inputs """
        self.dao.insert(product)

    def delete_product(self, product_id):
        """ Delete a product by ID """
        self.dao.delete(product_id)

    def shutdown(self):
        """ Close database connection """
        self.dao.close()
