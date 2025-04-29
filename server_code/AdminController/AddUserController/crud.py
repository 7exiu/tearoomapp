import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def add_product(name, description, price, image=None):
    try:
        
        app_tables.teas.add_row(
            name=name,
            description=description,
            price=price,
            image = image,
            is_available= True
            
           
        )
        print("✅ Produit ajouté à la base de données")
        return "Produit ajouté avec succès"
    
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout du produit : {e}")
        return f"Erreur lors de l'ajout du produit : {e}"
