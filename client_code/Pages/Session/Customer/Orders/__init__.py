from ._anvil_designer import OrdersTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state


class Orders(OrdersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_orders()

    # Any code you write here will run before the form opens.

  def load_orders(self):
    # Récupérer les commandes de l'utilisateur connecté
    user_id = anvil.server.call('get_user_info')['user_id']
    orders = anvil.server.call('get_user_orders', user_id)
    
    # Formater les données pour l'affichage
    formatted_orders = []
    for order in orders:
      formatted_orders.append({
        'id': f"Commande #{order['id']}",
        'created_at': order['time'].strftime("%d/%m/%Y %H:%M"),
        'status': "Réservé" if not order['is_available'] else "Disponible",
        'total_amount': f"{order['price']} €",
        'name': order['name'],
        'description': order['description']
      })
    
    self.orders_repeating_panel.items = formatted_orders

  def get_status_label(self, status):
    status_labels = {
      'pending': 'En attente',
      'processing': 'En cours de traitement',
      'shipped': 'Expédiée',
      'delivered': 'Livrée',
      'cancelled': 'Annulée'
    }
    return status_labels.get(status, status)

  def view_details_click(self, **event_args):
    # Récupérer l'ID de la commande sélectionnée
    order_id = event_args['sender'].item['id'].split('#')[1]
    # Charger la page de détails avec l'ID de la commande
    get_open_form().load_page('order_details', order_id=order_id)
