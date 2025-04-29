from ._anvil_designer import OrderDetailsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state

class OrderDetails(OrderDetailsTemplate):
  def __init__(self, order_id=None, **properties):
    self.init_components(**properties)
    if order_id:
      self.load_order_details(order_id)

  def load_order_details(self, order_id):
    # Récupérer les détails de la commande
    user_id = anvil.server.call('get_user_info')['user_id']
    order_details = anvil.server.call('get_order_details', order_id, user_id)
    
    if order_details:
      # Formater les données pour l'affichage
      formatted_order = {
        'id': f"Commande #{order_details['id']}",
        'created_at': order_details['time'].strftime("%d/%m/%Y %H:%M"),
        'status': "Réservé" if not order_details['is_available'] else "Disponible",
        'total_amount': f"{order_details['price']} €"
      }
      
      # Mettre à jour les champs de la commande
      self.order_id.text = formatted_order['id']
      self.order_date.text = formatted_order['created_at']
      self.order_status.text = formatted_order['status']
      self.order_total.text = formatted_order['total_amount']
      
      # Charger les détails du produit
      formatted_products = [{
        'name': order_details['name'],
        'quantity': "1",
        'price': f"{order_details['price']} €",
        'description': order_details['description']
      }]
      
      self.products_repeating_panel.items = formatted_products
    else:
      # Afficher un message d'erreur si la commande n'est pas trouvée
      Notification("Commande non trouvée", style="danger").show()
      get_open_form().load_page('orders')

  def get_status_label(self, status):
    status_labels = {
      'pending': 'En attente',
      'processing': 'En cours de traitement',
      'shipped': 'Expédiée',
      'delivered': 'Livrée',
      'cancelled': 'Annulée'
    }
    return status_labels.get(status, status) 