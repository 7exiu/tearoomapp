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
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#


'''
@anvil.server.callable
def addcard(product_id):
    # Rechercher le produit par ID dans la base de données
    product = app_tables.teas.get_by_id(product_id)

    if product is not None:
        print("=== Produit trouvé ===")
        print(f"ID         : {product.get_id()}")
        print(f"Nom        : {product['name']}")
        print(f"Prix       : {product['price']} €")
        print(f"Description: {product['description']}")
        print(f"Image      : {product['image']}")
        return product
    else:
        print("⚠️ Produit introuvable avec l'ID :", product_id)
        return None


'''
@anvil.server.callable
def addcard(product_id):
    # Rechercher le produit par ID dans la base de données
    article = app_tables.teas.get_by_id(product_id)

    if article is not None:
        print("=== Produit trouvé ===")
        identifiant = product_id
        app_tables.temp.add_row(
        name = article['name'],
        price = article['price'],
        image = article['image'], 
        description = article['description']
        )

        return identifiant
    else:
        print("⚠️ Produit introuvable avec l'ID :", product_id)
        return None


@anvil.server.callable
def reserve_table_for_user(user_id):
    """Réserve une table disponible pour un utilisateur donné (si disponible)."""
    try:
        if not user_id:
            raise ValueError("ID utilisateur manquant.")

        # Rechercher toutes les tables disponibles
        available_tables = app_tables.tables.search(is_available=True)

        if not available_tables:
            print("❌ Aucune table disponible.")
            return "Aucune table disponible pour le moment."

        # Réserver la première table disponible
        table = available_tables[0]
        table.update(
            is_available=False,
            reserved_by=user_id,
            reserved_at=datetime.now()
        )

        print(f"✅ Table réservée avec succès : ID={table.get_id()}")
        return table

    except Exception as e:
        print(f"❌ Erreur lors de la réservation de table : {e}")
        return f"Erreur : {e}"

@anvil.server.callable
def get_card():
  return list(app_tables.temp.search())