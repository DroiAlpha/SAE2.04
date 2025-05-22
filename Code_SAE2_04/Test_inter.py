from abc import ABC, abstractmethod
import unittest
class TestInterface(ABC, unittest.TestCase):
# ------------ Test Postgre ------------------------------------------#   

    # @abstractmethod
    def test_creation(self):
        pass

    # @abstractmethod
    def test_insertion(self):
        pass
    
   # @abstractmethod
    def test_affichage(self):
        pass

    # @abstractmethod
    def test_suppression(self):
        pass
