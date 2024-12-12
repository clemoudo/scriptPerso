import unittest
import os
import pandas as pd
from stock_manager.data_consolidator import DataConsolidator

class TestDataConsolidator(unittest.TestCase):
    def setUp(self):
        """
        Crée un environnement de test avec des fichiers CSV temporaires.
        """
        os.makedirs("test_csv", exist_ok=True)

        # Créer des fichiers CSV d'exemple
        data1 = pd.DataFrame({
            'name': ['Produit A', 'Produit B'],
            'category': ['Cat1', 'Cat2'],
            'quantity': [10, 5],
            'unit_price': [100.0, 200.0]
        })
        data2 = pd.DataFrame({
            'name': ['Produit C', 'Produit A'],
            'category': ['Cat1', 'Cat1'],
            'quantity': [15, 10],
            'unit_price': [150.0, 100.0]
        })
        data1.to_csv("test_csv/data1.csv", index=False)
        data2.to_csv("test_csv/data2.csv", index=False)

        self.consolidator = DataConsolidator()

    def tearDown(self):
        """
        Supprime les fichiers et répertoires temporaires créés pour les tests.
        """
        for file in os.listdir("test_csv"):
            os.remove(os.path.join("test_csv", file))
        os.rmdir("test_csv")

    def test_load_csv_files(self):
        """
        Vérifie que les fichiers CSV sont correctement chargés et consolidés.
        """
        self.consolidator.load_csv_files("test_csv")
        self.assertEqual(len(self.consolidator.data), 4)
        self.assertIn("name", self.consolidator.data.columns)

    def test_clean_data(self):
        """
        Vérifie que les données sont nettoyées (valeurs manquantes supprimées, types standardisés).
        """
        self.consolidator.load_csv_files("test_csv")
        self.consolidator.clean_data()

        # Vérifier les types
        self.assertTrue(pd.api.types.is_integer_dtype(self.consolidator.data["quantity"]))
        self.assertTrue(pd.api.types.is_float_dtype(self.consolidator.data["unit_price"]))

    def test_remove_duplicates(self):
        """
        Vérifie que les doublons sont supprimés correctement.
        """
        self.consolidator.load_csv_files("test_csv")
        self.consolidator.remove_duplicates()

        # Le produit "Produit A" en doublon doit être supprimé
        self.assertEqual(len(self.consolidator.data), 3)

    def test_get_data(self):
        """
        Vérifie que les données consolidées peuvent être récupérées correctement.
        """
        self.consolidator.load_csv_files("test_csv")
        data = self.consolidator.get_data()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
