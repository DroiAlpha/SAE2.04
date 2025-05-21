import threading
from Recup_Donnees import *

nom_ouvrage = "ouvrages"
nom_pt_prelevement = "pt_prelevement"
nom_commune = "commune"
nom_departement = "departement"

# ------------ SCRIPT POUR INSERTION -----------#
# A modifier s'il faut rajouter des tables, colonnes, ...

liste_colonnes_ouvrages = ['code_ouvrage', 'nom_ouvrage', 'date_exploitation_debut', 'date_exploitation_fin', 'code_type_milieu', 'libelle_departement', 'longitude', 'latitude', 'code_departement']
liste_type_colonnes_ouvrages = ['VARCHAR(300) PRIMARY KEY', 'VARCHAR(200)', 'DATE', 'DATE', 'VARCHAR(100)', 'VARCHAR(150)', 'DECIMAL(9,6)', 'DECIMAL(9,6)', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_pt_prelevement = ['code_point_prelevement', 'code_ouvrage', 'nom_point_prelevement', 'date_exploitation_debut', 'code_type_milieu', 'libelle_nature', 'code_departement']
liste_type_colonnes_pt_prelevement = ['VARCHAR(300) PRIMARY KEY', 'VARCHAR(200)', 'VARCHAR(200)', 'DATE', 'VARCHAR(100)', 'VARCHAR(150)', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_commune = ['nom_commune', 'code_commune_insee', 'code_departement']
liste_type_colonnes_commune = ['VARCHAR(500)', 'INTEGER PRIMARY KEY', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_departement = ['libelle_departement', 'code_departement']
liste_type_colonnes_departement = ['VARCHAR(500)', 'INTEGER PRIMARY KEY']


# ------------ Code pour supprimer ------------------------------------------#

# database_PostGre.supprimer(nom_pt_prelevement)
# database_PostGre.supprimer(nom_commune)
# database_PostGre.supprimer(nom_departement)
database_PostGre.supprimer(nom_ouvrage)

liste_valeurs_ouvrage1, liste_valeurs_ouvrage2 = split_list(liste_valeurs_ouvrage(liste_colonnes_ouvrages))

# ------------ SCRIPT POUR INSERTION (Les thread c'est pour que c'est plus rapide) -----------#

# Thread 1 : insère les départements
thread1 = threading.Thread(target=creation, args=(nom_departement, liste_colonnes_departement, liste_type_colonnes_departement, liste_valeurs_departement()))
thread1.start()
thread1.join()  # attendre que les départements soient insérés

# Thread 2,3,4 : insère les ouvrages et communes (indépendants entre eux) (3,4 sont tous les deux des ouvrages juste j'ai split pour que ça aille plus rapidement)
thread2 = threading.Thread(target=creation, args=(nom_ouvrage, liste_colonnes_ouvrages, liste_type_colonnes_ouvrages, liste_valeurs_ouvrage1))
thread3 = threading.Thread(target=creation, args=(nom_ouvrage, liste_colonnes_ouvrages, liste_type_colonnes_ouvrages, liste_valeurs_ouvrage2))
thread4 = threading.Thread(target=creation, args=(nom_commune, liste_colonnes_commune, liste_type_colonnes_commune, liste_valeurs_commune()))

thread2.start()
thread3.start()
thread4.start()

thread2.join()
thread3.join()
thread4.join()

# Thread 5 : pt_prelevement (dépend des ouvrages + départements)
thread5 = threading.Thread(target=creation, args=(nom_pt_prelevement, liste_colonnes_pt_prelevement, liste_type_colonnes_pt_prelevement, liste_valeurs_pt_prelevement(liste_colonnes_pt_prelevement)))
thread5.start()
thread5.join()













