import pandas as pd
import numpy as np

class Acces_API:
    def __init__(self, chemin):
        """
        Le chemin est l'URL de l'API
        """
        self.chemin = chemin

    def Tableau_valeurs(self):
        """
        Retourne un tableau contenant les données de l'API
        """
        url = self.chemin
        df = pd.read_json(url)
        info = df["data"]
        arr = np.array(info)
        return arr
    
    def Taille(self):
        return len(self.Tableau_valeurs()) 
    
    def colonnes(self):
        """
        Renvoie TOUTES les colonnes de la base de données
        De fait sert à rien mais bon c fun
        """
        L=[]
        for i in self.Tableau_valeurs()[0].keys():
            L.append(i)
        return L
    
    def valeurs(self, v, L_colonne: list):
        """
        Renvoie les valeurs de la base de données
        On parcourt en meme temps les clés et valeurs du fichier JSON
        On cherche ensuite les colonnes voulues
        Enfin, on ajoute les valeurs des colonnes à la liste à retourner
        (de fait pas utile mais bon c fun)
        """
        L=[]
        for k, val in self.Tableau_valeurs()[v].items(): 
            # -> .items : permet de parcourir en meme temps les clés et valeurs d'un dictionnaire
            for i in L_colonne:
                if k == i:
                    L.append(val)
        return L