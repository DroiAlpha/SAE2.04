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
    for i, elt in enumerate(valeurs):
        if len(elt) != len(colonnes):
            print(f"[ERREUR] Ligne {i} : {len(elt)} valeurs au lieu de {len(colonnes)} → {elt}")
            continue
        database_PostGre.inserer(table, elt, colonnes)
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

def liste_valeurs_commune():
    liste_PostGre = []
    set_PostGre = set()
    liste_colonne = ['nom_commune', 'code_commune_insee', 'code_departement']
    tableau = ouvrages.Tableau_valeurs()
    for i in range(len(tableau)):
        L = tuple(tableau[i].get(col, None) for col in liste_colonne)
        set_PostGre.add(L)
    tableau2 = pt_prelevement.Tableau_valeurs()
    for i in range(len(tableau2)):
        L = tuple(tableau2[i].get(col, None) for col in liste_colonne)
        set_PostGre.add(L)
    liste_PostGre = list(set_PostGre)
    return liste_PostGre

def liste_valeurs_departement():
    liste_PostGre = []
    set_PostGre = set()
    liste_colonne = ['libelle_departement', 'code_departement']
    tableau = ouvrages.Tableau_valeurs()
    for i in range(len(tableau)):
        L = tuple(tableau[i].get(col, None) for col in liste_colonne)
        set_PostGre.add(L)
    tableau2 = pt_prelevement.Tableau_valeurs()
    for i in range(len(tableau2)):
        L = tuple(tableau2[i].get(col, None) for col in liste_colonne)
        set_PostGre.add(L)
    liste_PostGre = list(set_PostGre)
    return liste_PostGre

# J'ai volé sur stackoverflow
def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

# ----------- VARIABLES IMPORTANTES --------------#

host = "localhost" # a mettre celui de PostGre
database = "uwu" # a mettre celui de PostGre
user = "postgres" # a mettre celui de PostGre
password = "lyna" # a mettre celui de PostGre

database_PostGre = PostGre(host, database, user, password)
