from ._anvil_designer import SignUpFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import math
import string
import time



class SignUpForm(SignUpFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.sign_up_form_buttons.submit_button.add_event_handler('click', self.on_submit_click)
    self.file_loader_1.file_types = ['.jpg', '.png']
      
  def on_submit_click(self, **event_args):
    photo = self.file_loader_1.file
    firstname = self.name_fields.firstname_field.text 
    lastname = self.name_fields.lastname_field.text
    email = self.credentials_fields.email_field.text
    password =self.credentials_fields.password_field.text
    confirmed_password = self.confirmed_password_field.text

    if not firstname or not lastname or not email or not password or not confirmed_password:
        Notification("Every field must be filled", style="danger").show()
        return

    if password != confirmed_password:
        Notification("The passwords are not identical", style="danger").show()
        return  

    entropie, taille_alphabet, redon = anvil.server.call('calculer_entropie', password)
    securite =  anvil.server.call('evaluer_securite', entropie)
    
    if redon < 60:
      Notification("The passwords is very so bad", style="danger").show()
      return
    if securite in ["Très faible", "Faible", "Moyenne"]:
        Notification(f"Password too weak: {securite} ({entropie:.2f} bits)", style="danger").show()
        return

    try:
        print(photo)
        photo = anvil.server.call("add_metadata", photo, email)
        print(photo)
        response = anvil.server.call('add_user', firstname, lastname, email, password, photo)
        Notification(response, style="success").show()

        self.name_fields.firstname_field.text = ""
        self.name_fields.lastname_field.text = ""
        self.credentials_fields.email_field.text = ""
        self.credentials_fields.password_field.text = ""
        self.confirmed_password_field.text = ""

        get_open_form().load_page("login")

    except Exception as e:
        Notification(f"Error while communicating with the server: {e}", style="danger").show()

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass
