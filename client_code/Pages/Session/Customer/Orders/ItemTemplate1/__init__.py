from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def table_card_booking_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def finish_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass
