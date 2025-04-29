from ._anvil_designer import LogInFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state

class LogInForm(LogInFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.form_buttons.submit_button.add_event_handler('click', self.on_submit_click)

  def on_submit_click(self, **event_args):
    print("✅ Tentative de connexion...")
    email = self.credentials_fields.email_field.text
    password = self.credentials_fields.password_field.text

    if not email or not password:
      Notification("Tous les champs doivent être remplis.", style="danger").show()
      return

    try:
      server_response = anvil.server.call('login_user', email, password)

      # Test si l'identifiant ou mot de passe est incorrect
      if server_response == "Invalid credentials":
        Notification("Email ou mot de passe incorrect.", style="danger").show()
        print("❌ Connexion refusée : identifiants invalides")
      else:
        Notification("Connexion réussie !", style="success").show()
        print("✅ Connexion réussie, chargement du dashboard...")
        get_open_form().load_page('dashboard')

    except Exception as e:
      print(f"❌ Erreur serveur lors de la connexion : {e}")
      Notification(f"Erreur lors de la connexion : {e}", style="danger").show()

  def form_hide(self, **event_args):
    pass

  def on_state_change(self):
    pass

  def sign_up_link_click(self, **event_args):
    get_open_form().load_page("signup")
