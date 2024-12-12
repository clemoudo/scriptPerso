import unittest
import pandas as pd
import os
from stock_manager.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        """
        Crée un environnement de test avec un DataFrame d'exemple.
        """
        self.sample_data = pd.DataFrame({
            'name': ['Produit A', 'Produit B', 'Produit C'],
            'category': ['Cat1', 'Cat2', 'Cat1'],
            'quantity': [10, 5, 2],
            'unit_price': [100.0, 200.0, 50.0]
        })
        self.report_generator = ReportGenerator(self.sample_data)

    def tearDown(self):
        """
        Nettoie les fichiers générés après les tests.
        """
        if os.path.exists("test_report.csv"):
            os.remove("test_report.csv")
        if os.path.exists("test_report.json"):
            os.remove("test_report.json")
        if os.path.exists("test_report.txt"):
            os.remove("test_report.txt")

    def test_calculate_total_stock_value(self):
        """
        Vérifie que la valeur totale des stocks est calculée correctement.
        """
        total_value = self.report_generator.calculate_total_stock_value()
        expected_value = (10 * 100.0) + (5 * 200.0) + (2 * 50.0)  # 1000 + 1000 + 100 = 2100
        self.assertEqual(total_value, expected_value)

    def test_count_products_by_category(self):
        """
        Vérifie que le nombre de produits par catégorie est calculé correctement.
        """
        counts = self.report_generator.count_products_by_category()
        self.assertEqual(counts['Cat1'], 2)
        self.assertEqual(counts['Cat2'], 1)

    def test_identify_critical_stock(self):
        """
        Vérifie que les produits en stock critique sont identifiés correctement.
        """
        critical_stock = self.report_generator.identify_critical_stock(threshold=10)
        self.assertEqual(len(critical_stock), 1)
        self.assertEqual(critical_stock.iloc[0]['name'], 'Produit C')

    def test_export_report_csv(self):
        """
        Vérifie que les rapports sont correctement exportés au format CSV.
        """
        self.report_generator.export_report(self.sample_data, "test_report.csv", file_format="csv")
        self.assertTrue(os.path.exists("test_report.csv"))

    def test_export_report_json(self):
        """
        Vérifie que les rapports sont correctement exportés au format JSON.
        """
        self.report_generator.export_report(self.sample_data, "test_report.json", file_format="json")
        self.assertTrue(os.path.exists("test_report.json"))

    def test_export_report_txt(self):
        """
        Vérifie que les rapports sont correctement exportés au format texte.
        """
        self.report_generator.export_report(self.sample_data, "test_report.txt", file_format="txt")
        self.assertTrue(os.path.exists("test_report.txt"))
