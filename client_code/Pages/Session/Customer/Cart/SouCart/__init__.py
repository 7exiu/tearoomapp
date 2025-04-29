from ._anvil_designer import SouCartTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import state

class SouCart(SouCartTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.form_show()

  def form_show(self, **event_args):
    try:
      # Récupérer toutes les cartes depuis la table temp
      cards = anvil.server.call('get_card')

      if not cards:
        print("❌ Aucune carte trouvée dans la table temp.")
        self.cart_name.text = "Aucune carte"
        return

      # Ici on prend simplement la première (ou tu peux faire une logique + avancée)
      cart = cards[0]
      print(">>> Carte chargée depuis la DB temp :", cart)

      # Nom
      self.cart_name.text = cart.get("name", "Nom inconnu")

      # Image
      img = cart.get("image")
      self.cart_image.source = img if isinstance(img, (Media, str)) else "https://placehold.co/200x150?text=Image+manquante"

      # Prix
      self.cart_price.text = f"{cart.get('price', 0)} €"

      # Date (optionnelle selon ta table)
      if "time" in cart and cart["time"]:
        self.cart_date.text = cart["time"].strftime("%d/%m/%Y %H:%M")
      else:
        self.cart_date.text = "Date non disponible"

    except Exception as e:
      print(f"❌ Erreur lors du chargement de la carte : {e}")
