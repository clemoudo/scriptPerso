import unittest
import pandas as pd
import os
from stock_manager.report_generator import ReportGenerator  # Replace with the correct module path

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        # Create test input file
        self.test_input_file = "test_stocks.csv"
        self.test_output_file = "test_rapport_inventaire.csv"

        test_data = {
            'Nom du Produit': ['Chaise', 'Table', 'Armoire', 'Chaise longue'],
            'Quantité': [10, 5, 3, 7],
            'Prix Unitaire': [20.0, 50.0, 100.0, 150.0],
            'Catégorie': ['Meubles', 'Meubles', 'Meubles', 'Extérieur']
        }
        pd.DataFrame(test_data).to_csv(self.test_input_file, index=False, encoding='utf-8')

    def tearDown(self):
        # Remove test files
        if os.path.exists(self.test_input_file):
            os.remove(self.test_input_file)
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    def test_report_generation(self):
        # Create ReportGenerator instance
        report_gen = ReportGenerator(self.test_input_file)

        # Generate and save the report
        report_gen.save_report(self.test_output_file)

        # Load the generated report
        generated_report = pd.read_csv(self.test_output_file)

        # Check report contents
        expected_data = {
            'Catégorie': ['Extérieur', 'Meubles', 'Toutes'],
            'Quantité_Totale': [7, 18, 25],
            'Valeur_Totale': [1050.0, 750.0, 1800.0]
        }
        expected_report = pd.DataFrame(expected_data)

        # Ensure the generated report matches the expected report
        pd.testing.assert_frame_equal(generated_report, expected_report)

if __name__ == '__main__':
    unittest.main()
