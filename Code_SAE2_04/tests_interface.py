"""
tests_interface.py : module pour les tests d'interface
# ? Adaptation des tests d'interface aux besoins de la classe Test
"""

from abc import ABC, abstractmethod
import unittest

class TestInterface(ABC, unittest.TestCase):
    """
    Classe abstraite pour les tests d'interface
    """

# -------------- Tests pour AccesAPI -------------- #
    
    @abstractmethod
    def test_tableau_valeurs(self):
        pass

    @abstractmethod
    def test_taille(self):
        pass

    @abstractmethod
    def test_colonnes(self):
        pass

    @abstractmethod
    def test_valeurs(self):
        pass

# -------------- Tests pour BasePostgres -------------- #

    @abstractmethod
    def test_creation(self):
        pass

    @abstractmethod
    def test_insertion(self):
        pass
    
    @abstractmethod
    def test_affichage(self):
        pass

    @abstractmethod
    def test_suppression(self):
        pass
        
# -------------- Tests pour RecupDonnees -------------- #

    @abstractmethod
    def test_liste_valeurs_ouvrage(self):
        pass
    
    @abstractmethod
    def test_liste_valeurs_pt_prelevement(self):
        pass
    
    @abstractmethod
    def test_liste_valeurs_commune(self):
        pass
    
    @abstractmethod
    def test_liste_valeurs_departement(self):
        pass
        
    @abstractmethod
    def test_diviser_liste(self):
        pass