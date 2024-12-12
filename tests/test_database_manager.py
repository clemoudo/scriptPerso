import unittest
import os
import pandas as pd
from stock_manager.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """
        Initialise une base de données SQLite temporaire pour les tests.
        """
        self.db_path = "test_stocks.sqlite"
        self.db_manager = DatabaseManager(self.db_path)
        self.db_manager.create_table()

    def tearDown(self):
        """
        Supprime la base de données temporaire après les tests.
        """
        self.db_manager.close_connection()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_table(self):
        """
        Vérifie que la table 'stocks' est créée correctement.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='stocks';"
        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'stocks')

    def test_insert_data(self):
        """
        Vérifie que les données peuvent être insérées dans la table.
        """
        sample_data = pd.DataFrame({
            'name': ['Produit A', 'Produit B'],
            'category': ['Cat1', 'Cat2'],
            'quantity': [10, 5],
            'unit_price': [100.0, 200.0]
        })
        self.db_manager.insert_data(sample_data)

        query = "SELECT * FROM stocks;"
        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1], 'Produit A')  # Vérifier le nom du premier produit

    def test_query_data(self):
        """
        Vérifie que les données peuvent être récupérées en fonction des critères spécifiés.
        """
        sample_data = pd.DataFrame({
            'name': ['Produit A', 'Produit B'],
            'category': ['Cat1', 'Cat2'],
            'quantity': [10, 5],
            'unit_price': [100.0, 200.0]
        })
        self.db_manager.insert_data(sample_data)

        criteria = {'category': 'Cat1'}
        results = self.db_manager.query_data(criteria)

        self.assertEqual(len(results), 1)
        self.assertEqual(results.iloc[0]['name'], 'Produit A')

    def test_update_data(self):
        """
        Vérifie que les données existantes peuvent être mises à jour.
        """
        sample_data = pd.DataFrame({
            'name': ['Produit A'],
            'category': ['Cat1'],
            'quantity': [10],
            'unit_price': [100.0]
        })
        self.db_manager.insert_data(sample_data)

        # Récupérer l'ID du produit
        query = "SELECT id FROM stocks WHERE name = 'Produit A';"
        cursor = self.db_manager.connection.cursor()
        cursor.execute(query)
        product_id = cursor.fetchone()[0]

        # Mettre à jour la quantité
        self.db_manager.update_data(product_id, {'quantity': 20})

        # Vérifier la mise à jour
        updated_data = self.db_manager.query_data({'id': product_id})
        self.assertEqual(updated_data.iloc[0]['quantity'], 20)

    def test_close_connection(self):
        """
        Vérifie que la connexion peut être fermée sans erreur.
        """
        try:
            self.db_manager.close_connection()
            self.assertTrue(True)  # Si aucune exception n'est levée, le test réussit
        except Exception as e:
            self.fail(f"Fermeture de la connexion échouée avec l'erreur : {e}")
