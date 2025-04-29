import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def get_user_orders(user_id):
    """
    Récupère toutes les commandes d'un utilisateur spécifique.
    """
    try:
        # Récupérer les commandes où l'utilisateur est le réservataire
        orders = app_tables.temp.search(
            tables.order_by("time", ascending=False),
            reserved_by=str(user_id)
        )
        return list(orders)
    except Exception as e:
        print(f"Erreur lors de la récupération des commandes: {e}")
        return []

@anvil.server.callable
def get_order_details(order_id, user_id):
    """
    Récupère les détails d'une commande spécifique.
    Vérifie que la commande appartient bien à l'utilisateur.
    """
    try:
        order = app_tables.temp.get(id=order_id)
        
        # Vérifier que la commande existe et appartient à l'utilisateur
        if not order or order['reserved_by'] != str(user_id):
            return None
            
        return {
            'id': order['id'],
            'name': order['name'],
            'description': order['description'],
            'price': order['price'],
            'time': order['time'],
            'is_available': order['is_available']
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de la commande: {e}")
        return None

@anvil.server.callable
def create_order(user_id, product_data):
    """
    Crée une nouvelle commande à partir des données du produit.
    """
    try:
        now = datetime.now()
        order = app_tables.temp.add_row(
            name=product_data['name'],
            price=product_data['price'],
            description=product_data.get('description', ''),
            time=now,
            is_available=False,
            reserved_by=str(user_id)
        )
        return order
    except Exception as e:
        print(f"Erreur lors de la création de la commande: {e}")
        return None 