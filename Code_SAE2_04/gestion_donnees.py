"""
gestion_donnees.py : module pour gérer les données dans une base de données PostGreSQL
# ? Ajout de commentaires
"""

import threading
from recup_donnees import *

# -------------- INITIALISATION -------------- #

# Noms des tables
nom_ouvrage = "ouvrage"
nom_pt_prelevement = "pt_prelevement"
nom_commune = "commune"
nom_departement = "departement"

# -------------- STRUCTURE DES TABLES -------------- #
# ! À modifier si vous voulez ajouter ou modifier des tables, colonnes...

liste_colonnes_ouvrage = ['code_ouvrage', 'nom_ouvrage', 'date_exploitation_debut', 'date_exploitation_fin', 'code_type_milieu', 'libelle_departement', 'longitude', 'latitude', 'code_departement']
liste_type_colonnes_ouvrage = ['VARCHAR(300) PRIMARY KEY', 'VARCHAR(200)', 'DATE', 'DATE', 'VARCHAR(100)', 'VARCHAR(150)', 'DECIMAL(9,6)', 'DECIMAL(9,6)', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_pt_prelevement = ['code_point_prelevement', 'code_ouvrage', 'nom_point_prelevement', 'date_exploitation_debut', 'code_type_milieu', 'libelle_nature', 'code_departement']
liste_type_colonnes_pt_prelevement = ['VARCHAR(300) PRIMARY KEY', 'VARCHAR(200)', 'VARCHAR(200)', 'DATE', 'VARCHAR(100)', 'VARCHAR(150)', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_commune = ['nom_commune', 'code_commune_insee', 'code_departement']
liste_type_colonnes_commune = ['VARCHAR(500)', 'INTEGER PRIMARY KEY', 'INTEGER REFERENCES departement(code_departement)']

liste_colonnes_departement = ['libelle_departement', 'code_departement']
liste_type_colonnes_departement = ['VARCHAR(500)', 'INTEGER PRIMARY KEY']

# -------------- CODE POUR SUPPRESSION DE TABLE -------------- #
# ! À décommenter si vous voulez supprimer les tables avant de les recréer...

# database_postgres.supprimer(nom_commune)
# database_postgres.supprimer(nom_departement)
# database_postgres.supprimer(nom_pt_prelevement)
# database_postgres.supprimer(nom_ouvrage)

liste_valeurs_ouvrage1, liste_valeurs_ouvrage2 = RecupDonnees.diviser_liste(RecupDonnees.liste_valeurs_ouvrage(liste_colonnes_ouvrage))

# -------------- SCRIPT POUR INSERTION DES DONNNÉES -------------- #
# Utilisation de threads pour insérer les données plus rapidement

# Thread 1 : insère les départements
thread1 = threading.Thread(target=RecupDonnees.creation, args=(nom_departement, liste_colonnes_departement, liste_type_colonnes_departement, RecupDonnees.liste_valeurs_departement()))
thread1.start()
thread1.join()  # ! Attendre que les départements soient insérés : les clés étrangères en dépendent

# Thread 2, 3 : insère les ouvrages (divise les ouvrages en deux threads pour améliorer la rapidité)
thread2 = threading.Thread(target=RecupDonnees.creation, args=(nom_ouvrage, liste_colonnes_ouvrage, liste_type_colonnes_ouvrage, liste_valeurs_ouvrage1))
thread3 = threading.Thread(target=RecupDonnees.creation, args=(nom_ouvrage, liste_colonnes_ouvrage, liste_type_colonnes_ouvrage, liste_valeurs_ouvrage2))
thread2.start()
thread3.start()
thread2.join()
thread3.join()

# Thread 4 : insère les communes
thread4 = threading.Thread(target=RecupDonnees.creation, args=(nom_commune, liste_colonnes_commune, liste_type_colonnes_commune, RecupDonnees.liste_valeurs_commune()))
thread4.start()
thread4.join()

# Thread 5 : insère les points de prélèvement (dépend des ouvrages et des départements)
thread5 = threading.Thread(target=RecupDonnees.creation, args=(nom_pt_prelevement, liste_colonnes_pt_prelevement, liste_type_colonnes_pt_prelevement, RecupDonnees.liste_valeurs_pt_prelevement(liste_colonnes_pt_prelevement)))
thread5.start()
thread5.join()