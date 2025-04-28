from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables
from ..Profile import Profile  # Import du formulaire Profile
from ..Cart import Cart  # Import du formulaire Cart
from ..Orders import Orders 
from ..Bookings import Bookings

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    print("🛠 Initialisation du Dashboard...")
    self.init_components(**properties)

    try:
      print("📡 Connexion au serveur pour récupérer les informations utilisateur...")
      self.user_info = anvil.server.call('get_user_info')
      print(f"✅ Infos utilisateur récupérées : {self.user_info}")

      if not self.user_info.get("user_email"):
        raise ValueError("Aucun email utilisateur récupéré.")

      print("🔎 Recherche de l'utilisateur dans la base de données...")
      self.user = anvil.server.call('get_user_by_email', self.user_info["user_email"])

      if not self.user:
        raise ValueError("Utilisateur introuvable dans la base de données.")

      print(f"🎯 Utilisateur trouvé : {self.user}")

      # Nettoyer l'ancien contenu du dashboard_panel
      print("🧹 Nettoyage du dashboard_panel...")
      self.dashboard_panel.clear()

      # Charger le formulaire Profile en passant l'utilisateur
      print("➕ Ajout du formulaire Profile au dashboard_panel...")
      profile_form = Profile(self.user)
      self.dashboard_panel.add_component(profile_form)

      print("✅ Formulaire Profile affiché avec succès dans le Dashboard.")

    except Exception as e:
      print(f"❌ Erreur dans Dashboard : {e}")
      Notification(f"Erreur lors du chargement du Dashboard : {e}", style="danger").show()

  def link_1_click(self, **event_args):
    """Méthode appelée lorsque le lien est cliqué"""
    bookings = Bookings()
    self.dashboard_panel.clear()  # On vide le panneau
    self.dashboard_panel.add_component(bookings)  # Exemple de contenu à afficher

  def cart_link_click(self, **event_args):
    """Méthode appelée lorsque le lien Cart est cliqué"""
    self.dashboard_panel.clear()  # On vide le panneau
    cart_form = Cart()  # On charge le formulaire Cart
    self.dashboard_panel.add_component(cart_form)  # On ajoute Cart au dashboard_panel

  def orders_link_click(self, **event_args):
    """Méthode appelée lorsque le lien Orders est cliqué"""
    self.dashboard_panel.clear()  # On vide le panneau
    orders_form = Orders()  # On charge le formulaire Orders
    self.dashboard_panel.add_component(orders_form)  # On ajoute Orders au dashboard_panel

  def profile_link_click(self, **event_args):
    """Méthode appelée lorsque le lien Profile est cliqué"""
    self.dashboard_panel.clear()  # On vide le panneau
    profile_form = Profile(self.user)  # On charge à nouveau le formulaire Profile
    self.dashboard_panel.add_component(profile_form)  # On ajoute Profile au dashboard_panel

  def link_2_click(self, **event_args):
    get_open_form().load_page("landing")
    pass
