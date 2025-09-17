"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
import sys
from dotenv import find_dotenv, load_dotenv
import mysql.connector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.product import Product

class ProductDAO:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
        try:
            env_file = find_dotenv()
            load_dotenv(env_file)   
            
            # Get database configuration from environment
            db_host = os.getenv("MYSQL_HOST", "localhost")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")     
            
            # Try to connect to the database
            self.conn = mysql.connector.connect(
                host=db_host, 
                user=db_user, 
                password=db_pass, 
                database=db_name
            )   
            self.cursor = self.conn.cursor()
            
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all products from MySQL """
        if not self.cursor:
            print("Erreur : Connexion à la base de données non établie")
            return []
        
        try:
            self.cursor.execute("SELECT id, name, brand, price FROM products ORDER BY id")
            rows = self.cursor.fetchall()
            
            products = []
            for row in rows:
                # Convert price from Decimal to float for consistency
                product = Product(id=row[0], name=row[1], brand=row[2], price=float(row[3]))
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Erreur lors de la sélection des produits : {e}")
            return []

    def insert(self, product):
        """ Insert given product into MySQL """
        if not self.cursor:
            print("Erreur : Connexion à la base de données non établie")
            return None
        
        try:
            self.cursor.execute(
                "INSERT INTO products (name, brand, price) VALUES (%s, %s, %s)",
                (product.name, product.brand, product.price),
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de l'insertion du produit : {e}")
            self.conn.rollback()
            return None

    def update(self, product):
        """ Update given product in MySQL """
        if not self.cursor:
            print("Erreur : Connexion à la base de données non établie")
            return
        
        try:
            self.cursor.execute(
                "UPDATE products SET name = %s, brand = %s, price = %s WHERE id = %s",
                (product.name, product.brand, product.price, product.id)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la mise à jour du produit : {e}")
            self.conn.rollback()

    def delete(self, product_id):
        """ Delete product from MySQL with given product ID """
        if not self.cursor:
            print("Erreur : Connexion à la base de données non établie")
            return
        
        try:
            self.cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression du produit : {e}")
            self.conn.rollback()

    def delete_all(self): #optional
        """ Empty products table in MySQL """
        if not self.cursor:
            print("Erreur : Connexion à la base de données non établie")
            return
        
        try:
            self.cursor.execute("DELETE FROM products")
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression de tous les produits : {e}")
            self.conn.rollback()
        
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
