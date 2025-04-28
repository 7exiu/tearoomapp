from ._anvil_designer import TableCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TableCard(TableCardTemplate):
    def __init__(self, **properties):
        # Initialisation des composants du formulaire.
        self.init_components(**properties)

        # Récupération de l'objet "item" (c'est la table qui a été passée au composant)
        tearoom_table = self.item
        
        # Remplir les labels avec les informations de la table
        self.table_card_title.text = tearoom_table["name"]  # Nom de la table
        self.table_card_is_available.text = "Available" if tearoom_table["is_available"] else "Not available"
        self.table_card_capacity.text = str(tearoom_table["chairs_count"]) + " people"  # Nombre de chaises

    def table_card_booking_button_click(self, **event_args):
        """Cette méthode est appelée lorsque le bouton de réservation est cliqué"""
        tearoom_table = self.item  # L'objet "table" que nous avons reçu
        
        # Vérification de la disponibilité de la table
        if not tearoom_table["is_available"]:
            Notification("Cette table n'est pas disponible pour la réservation.", style="danger").show()
            return

        # Appel d'une fonction serveur pour réserver la table (tu devras l'implémenter sur le serveur)
        try:
            reservation_response = anvil.server.call('reserve_table', tearoom_table["id"])  # Appel du serveur pour réserver la table
            if reservation_response == "success":
                Notification("Table réservée avec succès!", style="success").show()
                # Mettre à jour l'UI pour refléter que la table est maintenant réservée
                self.table_card_is_available.text = "Not available"
            else:
                Notification("Erreur lors de la réservation.", style="danger").show()
        except Exception as e:
            Notification(f"Erreur lors de la réservation : {e}", style="danger").show()

