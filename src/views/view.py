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

class View:
    @staticmethod
    def show_options():
        """ Show menu with operation options which can be selected by the user """
        while True:
            print("\n1. Gérer les utilisateurs\n2. Gérer les produits\n3. Quitter l'appli")
            choice = input("Choisissez une option: ")
            if choice == '1':
               UserView.show_options()
            elif choice == '2':
                ProductView.show_options()
            elif choice == '3':
                break
            else:
                print("Cette option n'existe pas.")