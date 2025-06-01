"""
acces_api.py : module pour accéder et manipuler les données d'une API au format JSON
# ? Ajout de commentaires et gestion des erreurs et des exceptions
"""

import pandas as pd
import numpy as np

class AccesAPI:
    """
    Classe permettant d'accéder et de manipuler les données d'une API au format JSON
    """
    def __init__(self, chemin_api: str):
        """
        Initialise le chemin d'accès à l'API avec son URL
        Paramètre : chemin_api (str) : URL de l'API
        """
        self.chemin_api = chemin_api

    def tableau_valeurs(self):
        """
        Charge et retourne les données de l'API (champ 'data') sous forme de tableau NumPy
        """
        try:
            df = pd.read_json(self.chemin_api) # Chargement du fichier JSON dans un DataFrame pandas
        except ValueError as e:
            print(f"[ERREUR] Impossible de charger les données depuis l'API : {e}")
            return np.array([])
        except FileNotFoundError as e:
            print(f"[ERREUR] Impossible de trouver l'API à l'URL {self.chemin_api} : {e}")
            return np.array([])
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors du chargement de l'API : {e}")
            return np.array([])
        
        if "data" not in df.columns:
            print(f"[ERREUR] Le champ 'data' n'existe pas dans les données de l'API")
            return np.array([])

        info = df["data"] # Liste des dictionnaires contenant les données de l'API
        arr = np.array(info) # Conversion de la liste de dictionnaires en tableau NumPy
        return arr
    
    def taille(self):
        """
        Retourne la taille ou nombre de lignes du tableau de valeurs de l'API
        """
        try:
            taille = len(self.tableau_valeurs())
        except ValueError as e:
            print(f"[ERREUR] Impossible de calculer la taille du tableau de valeurs : {e}")
            return 0
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors du calcul de la taille : {e}")
            return 0
        
        return taille
    
    def colonnes(self):
        """
        Retourne la liste de toutes les clés ou noms des colonnes de l'API
        """
        L = []
        
        try:
            for i in self.tableau_valeurs()[0].keys(): 
                L.append(i)
        except IndexError as e:
            print(f"[ERREUR] Impossible d'accéder aux données de l'API : {e}")
            return []
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de la récupération des colonnes : {e}")
            return []
        
        return L
    
    def valeurs(self, x, L_colonne: list):
        """
        Retourne la liste des valeurs correspondant aux colonnes voulues pour un enregistrement donné par son index
        Paramètres :
            -   x : index de l'enregistrement dans le tableau
            -   L_colonnes : liste des noms des colonnes à extraire
        """
        L = []

        try:
            # On parcourt en même temps les clés et valeurs du dictionnaire de l'enregistrement à l'indice donné
            for k, v in self.tableau_valeurs()[x].items(): 
                # -> .items : permet de parcourir en meme temps les clés et valeurs d'un dictionnaire
                for i in L_colonne:
                    # On vérifie si la clé (k) est dans la liste des colonnes voulues (liste_colonne)
                    # Si la clé correspond à une colonne voulue, on ajoute la valeur à la liste
                    if k == i:
                        L.append(v)
        except IndexError as e:
            print(f"[ERREUR] L'indice {x} est hors des limites du tableau de valeurs : {e}")
            return []
        except KeyError as e:
            print(f"[ERREUR] La clé {i} n'existe pas dans les données de l'API : {e}")
            return []
        except Exception as e:
            print(f"[ERREUR] Une erreur inattendue est survenue lors de la récupération des valeurs : {e}")
            return []
        
        return L