from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    tearoom_table = self.temp.tables 
    self.table_card_is_available.text = "Available" if tearoom_table["is_available"]  else 'Not available'
    self.table_card_capacity.text = str(tearoom_table["chairs_count"]) + " people"

    # Any code you write here will run before the form opens.
