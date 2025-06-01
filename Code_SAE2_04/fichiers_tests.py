"""
fichiers_tests.py : module pour générer des fichiers de test JSON simulant les données réelles de l'API Hub'eau (ouvrages, points de prélèvement, chroniques)
# ? Ajout d'un nouveau module de génération aléatoire de fichiers JSON pour automatiser les tests uniatires sur des jeux de données variés
"""

import json
import os
import random
from datetime import datetime, timedelta

class FichiersTests:
    """
    Classe utilitaire pour générer des fichiers de test mimant la structure réelle des données fournies par l'API Hub'eau
    """

    @staticmethod
    def generer_fichiers_ouvrages(nb_fichiers=100, dossier="tests_ouvrages"):
        """
        Génère des fichiers JSON pour les ouvrages
        """
        os.makedirs(dossier, exist_ok=True)
        for i in range(nb_fichiers):
            ouvrage = {
                "code_ouvrage": f"OPR{i:010d}",
                "nom_ouvrage": f"Ouvrage_{i}",
                "id_local_ouvrage": f"C_{random.randint(52000, 52999)}_{i}",
                "date_exploitation_debut": (datetime(1950, 1, 1) + timedelta(days=random.randint(0, 25000))).strftime("%Y-%m-%d"),
                "date_exploitation_fin": None,
                "code_precision_coord": str(random.randint(1, 9)),
                "libelle_precision_coord": "Coordonnées du centroïde de la commune",
                "commentaire": None,
                "code_commune_insee": str(random.randint(52000, 52999)),
                "nom_commune": random.choice(["Val-de-Meuse", "Chaumont", "Langres"]),
                "code_departement": "52",
                "libelle_departement": "Haute-Marne",
                "code_type_milieu": "SOUT",
                "libelle_type_milieu": "Souterrain",
                "longitude": round(random.uniform(5.0, 6.0), 6),
                "latitude": round(random.uniform(47.5, 48.5), 6),
                "codes_points_prelevements": [f"PTP{random.randint(100000, 999999)}"]
            }
            chemin = os.path.join(dossier, f"ouvrage_{i}.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump({"data": [ouvrage]}, f, ensure_ascii=False, indent=2)

    @staticmethod
    def generer_fichiers_points_prelevement(nb_fichiers=100, dossier="tests_points_prelevement"):
        """
        Génère des fichiers JSON pour les points de prélèvement
        """
        os.makedirs(dossier, exist_ok=True)
        for i in range(nb_fichiers):
            point = {
                "code_point_prelevement": f"PTP{random.randint(100000, 999999)}",
                "nom_point_prelevement": f"Point_{i}",
                "date_exploitation_debut": (datetime(1970, 1, 1) + timedelta(days=random.randint(0, 18000))).strftime("%Y-%m-%d"),
                "date_exploitation_fin": None,
                "code_type_milieu": "CONT",
                "libelle_type_milieu": "Surface continental",
                "code_nature": "F",
                "libelle_nature": "FICTIF",
                "code_commune_insee": str(random.randint(67000, 67999)),
                "nom_commune": "Gerstheim",
                "code_departement": "67",
                "libelle_departement": "Bas-Rhin",
                "nappe_accompagnement": random.choice([True, False]),
                "code_ouvrage": f"OPR{random.randint(1000000, 9999999)}"
            }
            chemin = os.path.join(dossier, f"pt_prelevement_{i}.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump({"data": [point]}, f, ensure_ascii=False, indent=2)

    @staticmethod
    def generer_fichiers_chroniques(nb_fichiers=100, dossier="tests_chroniques"):
        """
        Génère des fichiers JSON pour les chroniques de prélèvement
        """
        os.makedirs(dossier, exist_ok=True)
        for i in range(nb_fichiers):
            chronique = {
                "code_ouvrage": f"OPR{random.randint(1000000, 9999999)}",
                "annee": random.randint(2000, 2023),
                "volume": random.randint(1000, 20000),
                "code_usage": "AEP",
                "libelle_usage": "EAU POTABLE",
                "code_statut_volume": "1",
                "libelle_statut_volume": "Contrôlé Niveau 1",
                "code_qualification_volume": "1",
                "libelle_qualification_volume": "Correcte",
                "code_statut_instruction": "REA",
                "libelle_statut_instruction": "Prélèvement réalisé",
                "code_mode_obtention_volume": "MED",
                "libelle_mode_obtention_volume": "Mesure directe",
                "prelevement_ecrasant": False,
                "producteur_donnee": "AERM",
                "longitude": round(random.uniform(5.0, 6.0), 6),
                "latitude": round(random.uniform(47.5, 48.5), 6),
                "code_commune_insee": str(random.randint(52000, 52999)),
                "nom_commune": "Val-de-Meuse",
                "code_departement": "52",
                "libelle_departement": "Haute-Marne",
                "nom_ouvrage": f"COMMUNE_{random.randint(1, 100)}",
                "geometry": {
                    "type": "Point",
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                        }
                    },
                    "coordinates": [round(random.uniform(5.0, 6.0), 6), round(random.uniform(47.5, 48.5), 6)]
                },
                "uri_ouvrage": f"https://id.eaufrance.fr/OuvragePrel/OPR{random.randint(1000000, 9999999)}"
            }
            chemin = os.path.join(dossier, f"chronique_{i}.json")
            with open(chemin, "w", encoding="utf-8") as f:
                json.dump({"data": [chronique]}, f, ensure_ascii=False, indent=2)