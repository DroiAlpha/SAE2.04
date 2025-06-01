"""
tests.py : module de test des méthodes d'accès à l'API, de récupération et d'implémentation des données dans la base de données PostgreSQL
# ? Ajout de suggestions d'amélioration pour les tests de la classe BasePostgres (en bleu)
"""

import unittest
import os
import shutil
import numpy as np
from tests_interface import TestInterface
from acces_api import AccesAPI
from base_postgres import BasePostgres
from recup_donnees import RecupDonnees
from fichiers_tests import FichiersTests
import gestion_donnees

class Test(TestInterface, unittest.TestCase):
    """
    Classe de test des méthodes d'accès à l'API, de récupération et d'implémentation des données dans la base de données PostgreSQL
    """

# =========== Initialisation avant les tests =========== #

    # ----------- Initialisation avant Tests sur les APIs ----------- #
    # Définition des chemins d'accès aux APIs
    chemin_ouvrages = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/ouvrages"
    chemin_points_prelevement = "https://hubeau.eaufrance.fr/api/v1/prelevements/referentiel/points_prelevement"
    chemin_chroniques = "https://hubeau.eaufrance.fr/api/v1/chroniques"

    @classmethod
    def setUpClass(cls):
        """
        Initialise les paramètres requis pour les tests des méthodes des classes nécessaires
        """
        # ? ----------- Initialisation avant Tests pour BasePostgres ----------- #
        # ? Initialisation de la connexion à la base de données PostgreSQL (une fois au début de l'ensemble des tests / pas de chaque test)
        # ? cls.pg = BasePostgres("localhost", "test_db", "postgres", "password")
        # ? cls.conn = self.pg.connection()
        # ? cls.cur = self.conn.cursor()
        # ? cls.pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # ----------- Initialisation avant Tests sur les fichiers de tests ----------- #
        # Génération de 500 fichiers de tests pour chaque table de données
        cls.dossiers = {
            "ouvrages": "tests_ouvrages",
            "points_prelevement": "tests_points_prelevement",
            "chroniques": "tests_chroniques"
        }
        for nom, dossier in cls.dossiers.items():
            if not os.path.exists(dossier):
                if nom == "ouvrages":
                    FichiersTests.generer_fichiers_ouvrages(500, dossier)
                elif nom == "points_prelevement":
                    FichiersTests.generer_fichiers_points_prelevement(500, dossier)
                elif nom == "chroniques":
                    FichiersTests.generer_fichiers_chroniques(500, dossier)

    def acces_api(self, chemin_api):
        """
        Initialise les paramètres de connection à l'API pour les tests des méthodes de la classe AccesAPI
        Paramètre :
            -   chemin_api (str) : URL de l'API
        """
        # ----------- Initialisation avant Tests pour AccesAPI ----------- #
        self.api = AccesAPI(chemin_api)

# =========== Tests unitaires =========== #

    # ----------- Tests pour AccesAPI ----------- #

    def test_tableau_valeurs(self):
        """
        Test de la méthode tableau_valeurs
        """
        arr = self.api.tableau_valeurs()
        self.assertIsInstance(arr, np.ndarray, "Le tableau de valeurs doit être un tableau NumPy")
        self.assertGreater(len(arr), 0, "Le tableau de valeurs ne doit pas être vide")
        self.assertTrue(all(isinstance(row, dict) for row in arr), "Chaque ligne du tableau de valeurs doit être un dictionnaire")

    def test_taille(self):
        """
        Test de la méthode taille
        """
        taille = self.api.taille()
        self.assertIsInstance(taille, int, "La taille du tableau doit être un entier")
        self.assertGreater(taille, 0, "La taille du tableau doit être supérieure à 0")
        self.assertEqual(self.api.taille(), len(self.api.tableau_valeurs()), "La taille du tableau doit correspondre à son nombre de lignes")
    
    def test_colonnes(self):
        """
        Test de la méthode colonnes
        """
        colonnes = self.api.colonnes()
        self.assertIsInstance(colonnes, list, "Les colonnes doivent être une liste")
        self.assertGreater(len(colonnes), 0, "La liste des noms de colonnes ne doit pas être vide")
        self.assertTrue(all(isinstance(c, str) for c in colonnes), "Tous les noms de colonnes doivent être des chaînes de caractères")
        
    def test_valeurs(self):
        """
        Test de la méthode valeurs
        """
        colonnes = self.api.colonnes()
        if self.api.taille() > 0 and len(colonnes) > 0:
            valeurs = self.api.valeurs(0, colonnes[:2])
            self.assertIsInstance(valeurs, list, "Les valeurs doivent être une liste")
            self.assertGreater(len(valeurs), 0, "La liste des valeurs ne doit pas être vide")
            self.assertEqual(len(valeurs), len(colonnes[:2]), "Le nombre de valeurs doit correspondre au nombre de colonnes demandées")
            self.assertTrue(all(isinstance(v, (str, int, float)) for v in valeurs), "Toutes les valeurs doivent être des chaînes de caractères, entiers ou flottants")

    def lancer_test_acces_api(self):
        """
        Test de l'ensemble des méthodes d'accès à l'API
        """
        self.test_tableau_valeurs()
        self.test_taille()
        self.test_colonnes()
        self.test_valeurs()

    # ----------- Tests pour BasePostgres ----------- #

    def test_creation(self):
        """
        Test de la méthode creer_table
        """
        # Connexion à la base de données # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg = BasePostgres("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Vérification que la table a été créée
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='test_table')")
        self.assertTrue(cur.fetchone()[0])

        # Suppression de la table de test
        cur.execute("DROP TABLE test_table")
        conn.commit()

    def test_insertion(self):
        """
        Test de la méthode inserer
        """
        # Connexion à la base de données # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg = BasePostgres("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Vérification que la valeur a été insérée
        cur.execute("SELECT * FROM test_table WHERE id=1")
        row = cur.fetchone()
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], "Test")

        # Suppression de la table de test # ? Potentiellement déjà faite à la fin avec la méthode tearDownClass
        cur.execute("DROP TABLE test_table")
        conn.commit()
    
    def test_affichage(self):
        """
        Test de la méthode afficher
        """
        # Connexion à la base de données # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg = BasePostgres("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Affichage du contenu de la table de test
        pg.afficher("test_table", ["id", "name"])

        # Suppression de la table de test # ? Potentiellement déjà faite à la fin avec la méthode tearDownClass
        cur.execute("DROP TABLE test_table")
        conn.commit()
    
    def test_suppression(self):
        """
        Test de la méthode supprimer
        """
        # Connexion à la base de données # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg = BasePostgres("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test # ? Potentiellement déjà faite au début avec la méthode setUpClass
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Suppression de la table de test
        pg.supprimer("test_table")

        # Vérification que la table a été supprimée
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='test_table')")
        self.assertFalse(cur.fetchone()[0])

    # ----------- Tests pour RecupDonnees ----------- #

    def test_liste_valeurs_ouvrage(self):
        """
        Test de la méthode liste_valeurs_ouvrage
        """
        valeurs = RecupDonnees.liste_valeurs_ouvrage(gestion_donnees.liste_colonnes_ouvrage)
        self.assertIsInstance(valeurs, list, "La liste de valeurs n'est pas une liste")
        self.assertGreater(len(valeurs), 0, "La liste de valeurs est vide")

    def test_liste_valeurs_pt_prelevement(self):
        """
        Test de la méthode liste_valeurs_pt_prelevement
        """
        valeurs = RecupDonnees.liste_valeurs_pt_prelevement(gestion_donnees.liste_colonnes_pt_prelevement)
        self.assertIsInstance(valeurs, list, "La liste de valeurs n'est pas une liste")
        self.assertGreater(len(valeurs), 0, "La liste de valeurs est vide")

    def test_liste_valeurs_commune(self):
        """
        Test de la méthode liste_valeurs_commune
        """
        valeurs = RecupDonnees.liste_valeurs_commune()
        self.assertIsInstance(valeurs, list, "La liste de valeurs n'est pas une liste")
        self.assertGreater(len(valeurs), 0, "La liste de valeurs est vide")
        
    def test_liste_valeurs_departement(self):
        """
        Test de la méthode liste_valeurs_departement
        """
        valeurs = RecupDonnees.liste_valeurs_departement()
        self.assertIsInstance(valeurs, list, "La liste de valeurs n'est pas une liste")
        self.assertGreater(len(valeurs), 0, "La liste de valeurs est vide")
    
    def test_diviser_liste(self):
        """
        Test de la méthode diviser_liste
        """
        L = [1, 2, 3, 4, 5, 6]
        half = len(L) // 2
        L1, L2 = RecupDonnees.diviser_liste(L)
        self.assertEqual(L1, L[:half], "La première moitié de la liste est incorrecte")
        self.assertEqual(L2, L[half:], "La seconde moitié de la liste est incorrecte")

# =========== Tests sur les fichiers de tests =========== #

    def lancer_test_fichiers(self, dossier):
        """
        Test de l'accès aux fichiers JSON dans un dossier
        Paramètre :
            -   dossier (str) : chemin du dossier contenant les fichiers JSON
        """
        for fichier in os.listdir(dossier):
            chemin_fichier = os.path.join(dossier, fichier)
            self.acces_api(chemin_fichier)
            self.lancer_test_acces_api()

    def test_fichiers_ouvrages(self):
        """
        Test de l'accès aux fichiers JSON des ouvrages
        """
        dossier = self.dossiers["ouvrages"]
        self.lancer_test_fichiers(dossier)

    def test_fichiers_points_prelevement(self):
        """
        Test de l'accès aux fichiers JSON des points de prélèvement
        """
        dossier = self.dossiers["points_prelevement"]
        self.lancer_test_fichiers(dossier)

    def test_fichiers_chroniques(self):
        """
        Test de l'accès aux fichiers JSON des chroniques
        """
        dossier = self.dossiers["chroniques"]
        self.lancer_test_fichiers(dossier)

# =========== Tests sur les APIs =========== #

    def test_apis(self):
        """
        Test de l'accès aux APIs
        """
        # Test de l'API des ouvrages
        self.acces_api(self.chemin_ouvrages)
        self.lancer_test_acces_api()

        # Test de l'API des points de prélèvement
        self.acces_api(self.chemin_points_prelevement)
        self.lancer_test_acces_api()

        # Test de l'API des chroniques
        self.acces_api(self.chemin_chroniques)
        self.lancer_test_acces_api()

# =========== Nettoyage après les tests =========== #

    @classmethod
    def tearDownClass(cls):
        """
        Nettoyage requis après les tests : suppression de tables, fichiers et dossiers créés pour les tests des méthodes des classes nécessaires
        """
        # ? ----------- Nettoyage après Tests pour BasePostgres ----------- #
        # ? Suppression automatique de la table de test si elle existe (à la fin de l'ensemble des tests / pas de chaque test)
        # ? cls.cur.execute("DROP TABLE IF EXISTS test_table")
        # ? cls.conn.commit()

        # ----------- Nettoyage après Tests sur les fichiers de tests ----------- #
        # Suppression automatique de tous les dossiers et fichiers JSON créés pour les tests
        for dossier in cls.dossiers.values():
            if os.path.exists(dossier):
                shutil.rmtree(dossier)

# =========== Exécution des tests =========== #

if __name__ == "__main__":
    unittest.main()