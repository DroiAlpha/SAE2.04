"""
recup_donnees.py : module pour récupérer, importer définitivement et tester les données de l'API Hub'eau dans la base de données PostGreSQL
# ? Adaptation du module recup_donness à la POO avec la création d'une classe RecupDonnees
# ? Ajout de commentaires et gestion des erreurs et des exceptions
"""

# -------------- IMPORTATIONS, OBJETS ET MÉTHODES -------------- #

from acces_api import *
from base_postgres import *

class RecupDonnees:
    """
    Classe pour récupérer les données de l'API Hub'eau et les insérer dans la base de données PostgreSQL
    """

    # -------------- Initialisation -------------- #

    chemin_ouvrages = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/ouvrages"
    chemin_pt_prelevement = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/points_prelevement"

    ouvrages = AccesAPI(chemin_ouvrages) # -> 5000 lignes
    pt_prelevement = AccesAPI(chemin_pt_prelevement) # -> 5000 lignes

    # -------------- Méthodes -------------- #

    def creation(table: str, colonnes: list, type_colonnes: list, valeurs: list):
        """
        Crée une table et insére des valeurs dans la base de données PostgreSQL
        Paramètres :
            -   table (str) : nom de la table à créer
            -   colonnes (list) : liste des noms de colonnes
            -   type_colonnes (list) : liste des types de colonnes
            -   valeurs (list): liste des lignes de valeurs à insérer dans la table
        """
        try:
            database_postgres.creer_table(table, colonnes, type_colonnes)
            # Vérification de la longueur des valeurs
            for i, elt in enumerate(valeurs):
                if len(elt) != len(colonnes):
                    print(f"[ERREUR] Ligne {i} : {len(elt)} valeurs au lieu de {len(colonnes)} → {elt}")
                    continue
                try:
                    database_postgres.inserer(table, elt, colonnes)
                except Exception as e:
                    print(f"[ERREUR] Insertion impossible - Ligne {i} : {elt} → {e}")
            database_postgres.afficher(table, colonnes)
        except Exception as e:
            print(f"[ERREUR] Impossible de créer la table : {table} → {e}")

    def liste_valeurs_ouvrage(self, liste_colonnes: list):
        """
        Récupère les valeurs de l'API ouvrages et les retourne sous forme de liste
        Paramètre :
            -   liste_colonnes : liste des colonnes à récupérer
        """
        liste_postgres = []

        try:
            tableau = self.ouvrages.tableau_valeurs()
            # Pour chaque ligne du tableau, on crée une liste des valeurs des colonnes demandées et on l'ajoute à la liste finale
            for i in range(len(tableau)):
                L = []
                for col in liste_colonnes:
                    L.append(tableau[i].get(col, None))
                liste_postgres.append(L)
            return liste_postgres
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les données de l'API ouvrages → {e}")
            return None

    def liste_valeurs_pt_prelevement(self, liste_colonnes: list):
        """
        Récupère les valeurs de l'API points de prélèvement et les retourne sous forme de liste
        Paramètre :
            -   liste_colonnes : liste des colonnes à récupérer
        """
        liste_postgres = []
        
        try:
            tableau = self.pt_prelevement.tableau_valeurs()
            # Pour chaque ligne du tableau, on crée une liste des valeurs des colonnes demandées et on l'ajoute à la liste finale
            for i in range(len(tableau)):
                L = []
                for col in liste_colonnes:
                    L.append(tableau[i].get(col, None))
                liste_postgres.append(L)
            return liste_postgres
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les données de l'API points de prélèvement → {e}")
            return None

    def liste_valeurs_commune(self):
        """
        Récupère les valeurs de l'API ouvrages et points de prélèvement pour les communes et les retourne sous forme de liste
        """
        liste_postgres = []
        
        try:
            set_postgres = set()
            liste_colonnes = ['nom_commune', 'code_commune_insee', 'code_departement']
            tableau = self.ouvrages.tableau_valeurs()
            # Pour chaque ligne du tableau, on crée une liste des valeurs des colonnes demandées et on l'ajoute à un set pour éviter les doublons
            for i in range(len(tableau)):
                L = tuple(tableau[i].get(col, None) for col in liste_colonnes)
                set_postgres.add(L)
            tableau2 = self.pt_prelevement.tableau_valeurs()
            # On fait la même chose pour les points de prélèvement
            for i in range(len(tableau2)):
                L = tuple(tableau2[i].get(col, None) for col in liste_colonnes)
                set_postgres.add(L)
            liste_postgres = list(set_postgres)
            return liste_postgres
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les données sur les communes → {e}")
            return None

    def liste_valeurs_departement(self):
        """
        Récupère les valeurs de l'API ouvrages et points de prélèvement pour les départements et les retourne sous forme de liste
        """
        liste_postgres = []

        try:
            set_postgres = set()
            liste_colonnes = ['libelle_departement', 'code_departement']
            tableau = self.ouvrages.tableau_valeurs()
            # Pour chaque ligne du tableau, on crée une liste des valeurs des colonnes demandées et on l'ajoute à un set pour éviter les doublons
            for i in range(len(tableau)):
                L = tuple(tableau[i].get(col, None) for col in liste_colonnes)
                set_postgres.add(L)
            tableau2 = self.pt_prelevement.tableau_valeurs()
            # On fait la même chose pour les points de prélèvement
            for i in range(len(tableau2)):
                L = tuple(tableau2[i].get(col, None) for col in liste_colonnes)
                set_postgres.add(L)
            liste_postgres = list(set_postgres)
            return liste_postgres
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les données sur les départements → {e}")
            return None

    def diviser_liste(L):
        """
        Divise une liste en deux moitiés
        Paramètre : 
            -   L : liste à diviser
        Retourne :
            -   Deux listes, la première moitié et la seconde moitié de la liste d'origine
        """
        try:
            half = len(L)//2
            return L[:half], L[half:]
        except Exception as e:
            print(f"[ERREUR DIVISION LISTE] → {e}")
            return None

# -------------- VARIABLES IMPORTANTES -------------- #

# ! À adapter avec les informations de la base de données PostgreSQL
host = "localhost"
database = "postgres_db"
user = "postgres_user"
password = "password"

database_postgres = BasePostgres(host, database, user, password)