"""
Main view for the store manager application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import sys
import os

from views.product_view import ProductView
from views.user_view import UserView
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.product_controller import ProductController
from controllers.user_controller import UserController
from models.product import Product
from models.user import User

class View:
    @staticmethod
    def show_options():
        """ Show menu with operation options which can be selected by the user """
        user_controller = UserController()
        product_controller = ProductController()
        
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Montrer la liste d'utilisateurs")
            print("2. Ajouter un utilisateur")
            print("3. Montrer la liste d'articles")
            print("4. Ajouter un article")
            print("5. Quitter l'appli")
            
            choice = input("Choisissez une option: ")
            
            if choice == '1':
                # Voir la liste d'utilisateurs
                users = user_controller.list_users()
                UserView.show_users(users)
            elif choice == '2':
                # Remplir formulaire d'utilisateur et ajouter
                name, email = UserView.get_inputs()
                user = User(None, name, email)
                user_controller.create_user(user)
                print("Utilisateur ajouté avec succès!")
            elif choice == '3':
                # Voir la liste d'articles
                products = product_controller.list_products()
                ProductView.show_products(products)
            elif choice == '4':
                # Remplir formulaire d'article et ajouter
                name, brand, price = ProductView.get_inputs()
                product = Product(None, name, brand, price)
                product_controller.create_product(product)
                print("Article ajouté avec succès!")
            elif choice == '5':
                # Quitter l'appli
                user_controller.shutdown()
                product_controller.shutdown()
                print("Au revoir!")
                break
            else:
                print("Cette option n'existe pas.")