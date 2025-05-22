# Test de PostGre.py
import unittest
from PostGre import *
from Test_inter import TestInterface
class Test(TestInterface, unittest.TestCase):
    def test_creation(self):
        """
        Test de la méthode creer_table
        """
        # Connexion à la base de données
        pg = PostGre("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test
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
        # Connexion à la base de données
        pg = PostGre("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Vérification que la valeur a été insérée
        cur.execute("SELECT * FROM test_table WHERE id=1")
        row = cur.fetchone()
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], "Test")

        # Suppression de la table de test
        cur.execute("DROP TABLE test_table")
        conn.commit()
    
    def test_affichage(self):
        """
        Test de la méthode afficher
        """
        # Connexion à la base de données
        pg = PostGre("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Affichage du contenu de la table de test
        pg.afficher("test_table", ["id", "name"])

        # Suppression de la table de test
        cur.execute("DROP TABLE test_table")
        conn.commit()
    
    def test_suppression(self):
        """
        Test de la méthode supprimer
        """
        # Connexion à la base de données
        pg = PostGre("localhost", "test_db", "postgres", "password")
        conn = pg.connection()
        cur = conn.cursor()

        # Création d'une table de test
        pg.creer_table("test_table", ["id", "name"], ["INTEGER PRIMARY KEY", "VARCHAR(100)"])

        # Insertion d'une valeur dans la table de test
        pg.inserer("test_table", (1, "Test"), ["id", "name"])

        # Suppression de la table de test
        pg.supprimer("test_table")

        # Vérification que la table a été supprimée
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='test_table')")
        self.assertFalse(cur.fetchone()[0])
    
if __name__ == "__main__":
    unittest.main()