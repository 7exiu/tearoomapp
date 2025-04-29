import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import math
import string
import re

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
@anvil.server.callable
def calculer_entropie(mot_de_passe):
    """
    Calcule l'entropie d'un mot de passe en bits.
    
    Args:
        mot_de_passe (str): Le mot de passe à analyser
    
    Returns:
        tuple: (entropie en bits, taille de l'alphabet utilisé, redon)
    """
    # Vérifications de base
    if len(mot_de_passe) < 12:
        return 0, 0, 0  # Mot de passe trop court
    
    # Vérification des caractères requis
    has_upper = bool(re.search(r'[A-Z]', mot_de_passe))
    has_lower = bool(re.search(r'[a-z]', mot_de_passe))
    has_digit = bool(re.search(r'\d', mot_de_passe))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', mot_de_passe))
    
    if not (has_upper and has_lower and has_digit and has_special):
        return 0, 0, 0  # Manque des types de caractères requis
    
    # Vérification des séquences répétitives
    if re.search(r'(.)\1{2,}', mot_de_passe):
        return 0, 0, 0  # Trop de répétitions
    
    # Calcul de l'entropie
    minuscules = set(string.ascii_lowercase)
    majuscules = set(string.ascii_uppercase)
    chiffres = set(string.digits)
    symboles = set(string.punctuation)
    
    taille_alphabet = 0
    if any(c in minuscules for c in mot_de_passe):
        taille_alphabet += 26
    if any(c in majuscules for c in mot_de_passe):
        taille_alphabet += 26
    if any(c in chiffres for c in mot_de_passe):
        taille_alphabet += 10
    if any(c in symboles for c in mot_de_passe):
        taille_alphabet += 32
    
    entropie = len(mot_de_passe) * math.log2(taille_alphabet)
    taille = len(mot_de_passe)
    redon = (taille * math.log2(taille_alphabet)) - entropie

    return entropie, taille_alphabet, redon
    
@anvil.server.callable
def evaluer_securite(entropie):
    """
    Évalue la sécurité d'un mot de passe basée sur son entropie.
    
    Args:
        entropie (float): L'entropie du mot de passe en bits
        
    Returns:
        str: Niveau de sécurité
    """
    if entropie == 0:
        return "Invalide"
    elif entropie < 60:
        return "Très faible"
    elif entropie < 80:
        return "Faible"
    elif entropie < 100:
        return "Moyenne"
    elif entropie < 120:
        return "Forte"
    else:
        return "Très forte"

  
