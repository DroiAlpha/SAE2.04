from abc import ABC, abstractmethod
import unittest
class TestInterface(ABC, unittest.TestCase):
    
# ------------ Test Postgre ------------------------------------------#   

    @abstractmethod
    def test_insertion(self):
        pass
    
    @abstractmethod
    def test_suppression(self):
        pass
    
    @abstractmethod
    def test_creation(self):
        pass
        
# ------------ Test Méthodes de Recup_Donnees ------------------------------------------#

    @abstractmethod
    def Test_liste_valeurs_ouvrage(self):
        pass
    
    @abstractmethod
    def Test_liste_valeurs_pt_prelevement(self):
        pass
    
    @abstractmethod
    def Test_liste_valeurs_commune(self):
        pass
    
    @abstractmethod
    def Test_liste_valeurs_departement(self):
        pass
        
    @abstractmethod
    def Test_split_list(self):
        pass
        
# ------------ Test Appels/Acces a l'API------------------------------------------#  
    @abstractmethod
    def Test_Acces_API(self):
        pass
