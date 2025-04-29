import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from argon2 import PasswordHasher

@anvil.server.callable
def login_user(email, password):
    print(f"🔑 Tentative de connexion pour l'email : {email}")
    user = app_tables.users.get(email=email)
    ph = PasswordHasher()
    
    if user is None:
        print(f"❌ Utilisateur non trouvé pour l'email : {email}")
        return "Invalid credentials"

    try:
        is_password_valid = ph.verify(user['password'], password)
        if not is_password_valid:
            print(f"❌ Mot de passe incorrect pour l'email : {email}")
            return "Invalid credentials"

        set_user_info(user['email'], user.get_id())
        print(f"✅ Connexion réussie pour : {user['firstname']} {user['lastname']}")
        return f"Welcome back {user['firstname']} {user['lastname']}"
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du mot de passe : {e}")
        return "Invalid credentials"


@anvil.server.callable
def logout_user():
  print(f"SESSION ITEMS: {anvil.server.session}")
  anvil.server.session.clear()
  print(f"SESSION ITEMS: {anvil.server.session}")
  
@anvil.server.callable
def set_user_info(email, id):
    anvil.server.session['user_email'] = email
    anvil.server.session['user_id'] = id
    print(f"✅ SESSION ITEMS INITIALIZED: {anvil.server.session})")

@anvil.server.callable  
def get_all_users():
  print("📋 Récupération de tous les utilisateurs...")
  return list(app_tables.users.search())

@anvil.server.callable
def get_user_info():
    return {"user_email":anvil.server.session.get('user_email'), "user_id":anvil.server.session.get('user_id')}
