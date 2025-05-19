"""
Fichier pour tester, et après mettre definitivement les valeurs
dans la database
"""

# -------------- IMPORTATIONS, OBJETS ET FONCTIONS -----------------#

from PostGre import *
from Acces_API import *

url_ouvrages = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/ouvrages"
url_pt_prelevement = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/points_prelevement"

ouvrages = Acces_API(url_ouvrages) # -> 5000 lignes
pt_prelevement = Acces_API(url_pt_prelevement) # -> 5000 lignes

def creation(table: str, colonnes: list, type_colonnes: list, valeurs: list):
    database_PostGre.creer_table(table, colonnes, type_colonnes)
    for elt in valeurs:
        database_PostGre.inserer(table, elt)
    database_PostGre.afficher(table, colonnes)

def liste_valeurs_ouvrage(liste_colonne: list): # les valeurs de l'API ouvrages
    liste_PostGre = []
    tableau = ouvrages.Tableau_valeurs()
    for i in range(len(tableau)):
        L = []
        for col in liste_colonne:
            L.append(tableau[i].get(col, None))
        liste_PostGre.append(L)
    return liste_PostGre

def liste_valeurs_pt_prelevement(liste_colonne: list): # les valeurs de l'API points de prelevement
    liste_PostGre = []
    tableau = pt_prelevement.Tableau_valeurs()
    for i in range(len(tableau)):
        L = []
        for col in liste_colonne:
            L.append(tableau[i].get(col, None))
        liste_PostGre.append(L)
    return liste_PostGre

# ----------- VARIABLES IMPORTANTES --------------#

host = "localhost" # a mettre celui de PostGre
database = "Test" # a mettre celui de PostGre
user = "postgres" # a mettre celui de PostGre
password = "2704" # a mettre celui de PostGre

database_PostGre = PostGre(host, database, user, password)

nom_ouvrage = "ouvrages"
nom_pt_prelevement = "pt_prelevement"

# --------------- TEST ----------------#

# -----Test pour acces à l'API -------#
liste_ouvrages = liste_valeurs_ouvrage(ouvrages.colonnes())
liste_pt_prelevement = liste_valeurs_pt_prelevement(pt_prelevement.colonnes())

# print(liste_ouvrages)
# print("")
# print(liste_pt_prelevement)
# print("")
assert len(liste_ouvrages) == ouvrages.Taille()
assert len(liste_pt_prelevement) == pt_prelevement.Taille()
print("Taille data ouvrage :", len(liste_ouvrages))
print("Taille data point prelevement :",len(liste_pt_prelevement))
print("")

# --------Test pour acces à PostGre -----------#
table = "Personne"
colonne = ["Nom", "Prenom", "Age"]
type_colonne = ["VARCHAR(20)", "VARCHAR(20)", "INTEGER"]
liste_personne = [["DELACOUX", "Amaury", 19], ["GUERROUAH", "Massinissa", 19], ["CASTANO", "Theo", 18], ["KOY", "Willy", 19], ["LAHLOU", "Ilyas", 20]]

database_PostGre.supprimer(table)

creation(table, colonne, type_colonne, liste_personne)

# ------------ SCRIPT POUR INSERTION -----------#
# A modifier s'il faut rajouter des tables, colonnes, ...

liste_colonnes_ouvrages = [] # a remplir avec les colonnes choisies pour ouvrage
liste_type_colonnes_ouvrages = [] # a remplir avec les types des colonnes pour ouvrage

liste_colonnes_pt_prelevement = [] # a remplir avec les colonnes chosies pour pt_prelevement
liste_type_colonnes_pt_prelevement = [] # a remplir avec les types des colonnes pour pt_prelevement

# creation(nom_ouvrage, liste_colonnes_ouvrages, liste_type_colonnes_ouvrages, liste_valeurs_ouvrage(liste_colonnes_ouvrages))

# creation(nom_pt_prelevement, liste_colonnes_pt_prelevement, liste_type_colonnes_pt_prelevement, liste_valeurs_pt_prelevement(liste_colonnes_pt_prelevement))