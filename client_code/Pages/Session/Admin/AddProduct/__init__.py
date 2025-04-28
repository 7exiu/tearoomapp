from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class AddProduct(AddProductTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def add_pd_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
