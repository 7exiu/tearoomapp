import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def get_cart(user_id):
    """
    Récupère le panier d'un utilisateur.
    """
    cart = app_tables.carts.get(user_id=user_id)
    if cart:
        return {
            'id': cart['id'],
            'content': cart['content'],
            'total_amount': cart['total_amount']
        }
    return None

@anvil.server.callable
def update_cart(user_id, cart_data):
    """
    Met à jour le panier d'un utilisateur.
    """
    cart = app_tables.carts.get(user_id=user_id)
    if cart:
        cart['content'] = cart_data
        cart['total_amount'] = sum(item['price'] * item['quantity'] for item in cart_data)
        cart['update_at'] = datetime.now()
    else:
        app_tables.carts.add_row(
            user_id=user_id,
            content=cart_data,
            total_amount=sum(item['price'] * item['quantity'] for item in cart_data),
            created_at=datetime.now(),
            update_at=datetime.now()
        )

@anvil.server.callable
def delete_cart(user_id):
    """
    Supprime le panier d'un utilisateur.
    """
    cart = app_tables.carts.get(user_id=user_id)
    if cart:
        cart.delete()

@anvil.server.callable
def create_cart(data):
  now = datetime.now()
  app_tables.carts.add_row(   
    content=data, 
    created_at=now, 
    update_at=now,
    total_amount=data["total_amount"]
  )
  