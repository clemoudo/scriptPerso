import unittest
import os
import pandas as pd
from stock_manager.stock_manager import *

class TestStockManager(unittest.TestCase):
    def setUp(self):
        """
        Initialise une base SQLite et un environnement de test pour le gestionnaire de stocks.
        """
        self.db_path = "test_stocks.sqlite"
        self.csv_dir = "test_csv"
        os.makedirs(self.csv_dir, exist_ok=True)

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
        data1.to_csv(f"{self.csv_dir}/data1.csv", index=False)
        data2.to_csv(f"{self.csv_dir}/data2.csv", index=False)

        self.stock_manager = StockManager(self.db_path)
        self.stock_manager.initialize_database()

    def tearDown(self):
        """
        Supprime les fichiers et la base de données après les tests.
        """
        self.stock_manager.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        for file in os.listdir(self.csv_dir):
            os.remove(os.path.join(self.csv_dir, file))
        os.rmdir(self.csv_dir)

    def test_initialize_database(self):
        """
        Vérifie que la base de données est initialisée avec une table valide.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='stocks';"
        cursor = self.stock_manager.db_manager.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'stocks')

    def test_consolidate_files(self):
        """
        Vérifie que les fichiers CSV sont consolidés et insérés dans la base de données.
        """
        self.stock_manager.consolidate_files(self.csv_dir)
        query = "SELECT * FROM stocks;"
        cursor = self.stock_manager.db_manager.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Vérifie que les données consolidées contiennent les bonnes informations
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][1], 'Produit A')  # Nom du premier produit

    def test_search_products(self):
        """
        Vérifie que la recherche multicritères retourne les bons résultats.
        """
        self.stock_manager.consolidate_files(self.csv_dir)
        criteria = {'category': 'Cat1'}
        results = self.stock_manager.search_products(criteria)

        # Vérifie que les résultats de la recherche sont corrects
        self.assertEqual(len(results), 2)
        self.assertIn('Produit A', results['name'].values)

    def test_generate_report(self):
        """
        Vérifie que les rapports sont générés et exportés correctement.
        """
        self.stock_manager.consolidate_files(self.csv_dir)
        export_path = "test_report.csv"

        self.stock_manager.generate_report("summary", export_path, "csv")
        self.assertTrue(os.path.exists(export_path))

        # Nettoyage après test
        if os.path.exists(export_path):
            os.remove(export_path)
