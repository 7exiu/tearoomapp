from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ..Profile import Profile
from ..Cart import Cart
from ..Orders import Orders
from ..Bookings import Bookings
from ...Admin.Dashboard_admin import Dashboard_admin
from .... import state

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_page = None
    self.load_profile()  # Charger automatiquement le Profile

  def load_profile(self):
    """Charge la page Profile dans le dashboard."""
    self.current_page = Profile()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('profile_link')

  def load_cart(self):
    """Charge la page Cart dans le dashboard."""
    self.current_page = Cart()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('cart_link_copy')

  def load_orders(self):
    """Charge la page Orders dans le dashboard."""
    self.current_page = Orders()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('orders_link_copy')

  def load_bookings(self):
    """Charge la page Bookings dans le dashboard."""
    self.current_page = Bookings()
    self.dashboard_panel.clear()
    self.dashboard_panel.add_component(self.current_page)
    self.update_navigation_style('link_1')

  def update_navigation_style(self, active_link):
    """Met à jour le style des liens de navigation."""
    links = [
      'profile_link',
      'cart_link_copy',
      'orders_link_copy',
      'link_1'
    ]
    
    for link in links:
      getattr(self, link).role = 'selected' if link == active_link else ''

  def profile_link_click(self, **event_args):
    self.load_profile()

  def cart_link_click(self, **event_args):
    self.load_cart()

  def orders_link_click(self, **event_args):
    self.load_orders()

  def link_1_click(self, **event_args):
    self.load_bookings()

  def link_2_click(self, **event_args):
    """Redirige vers la page Menu (hors du dashboard)."""
    get_open_form().load_page('menu')

  def menu_button_click(self, **event_args):
    """Redirige vers la page Menu (hors du dashboard)."""
    get_open_form().load_page('menu')

  def link_3_click(self, **event_args):
    """Redirige vers le dashboard admin."""
    get_open_form().load_page('dashboard_admin')
