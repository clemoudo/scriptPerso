import unittest
import pandas as pd
import os
from stock_manager.import_CSV import ImportCSV, ColumnNameError, ColumnTypeError, EmptyCellError

class TestImportCSV(unittest.TestCase):
    def setUp(self):
        # Fichiers de test CSV
        self.database_file = "test_database.csv"
        self.new_data_file = "test_new_data.csv"

        # Créer un fichier de base de données CSV
        database_data = {
            'Nom du Produit': ['Chaise', 'Table'],
            'Quantité': [10, 5],
            'Prix Unitaire': [20.0, 50.0],
            'Catégorie': ['Meubles', 'Meubles']
        }
        pd.DataFrame(database_data).to_csv(self.database_file, index=False, encoding='utf-8')

    def tearDown(self):
        # Supprimer les fichiers de test
        if os.path.exists(self.database_file):
            os.remove(self.database_file)
        if os.path.exists(self.new_data_file):
            os.remove(self.new_data_file)

    def test_valid_merge(self):
        # Données valides pour le nouveau fichier CSV
        new_data = {
            'Nom du Produit': ['Armoire'],
            'Quantité': [3],
            'Prix Unitaire': [100.0],
            'Catégorie': ['Meubles']
        }
        pd.DataFrame(new_data).to_csv(self.new_data_file, index=False, encoding='utf-8')

        # Tester la fusion
        importer = ImportCSV(self.new_data_file, self.database_file)
        importer.merge_data()

        # Vérifier que la base de données a été mise à jour
        updated_data = pd.read_csv(self.database_file, encoding='utf-8')
        self.assertEqual(len(updated_data), 3)  # 2 initial + 1 nouveau
        self.assertIn('Armoire', updated_data['Nom du Produit'].values)

    def test_column_name_mismatch(self):
        # Fichier CSV avec noms de colonnes incorrects
        invalid_data = {
            'Product Name': ['Armoire'],
            'Quantité': [3],
            'Prix Unitaire': [100.0],
            'Catégorie': ['Meubles']
        }
        pd.DataFrame(invalid_data).to_csv(self.new_data_file, index=False, encoding='utf-8')

        importer = ImportCSV(self.new_data_file, self.database_file)

        with self.assertRaises(ColumnNameError):
            importer.merge_data()

    def test_column_type_mismatch(self):
        # Fichier CSV avec types de colonnes incorrects
        invalid_data = {
            'Nom du Produit': ['Armoire'],
            'Quantité': ['Trois'],  # Texte au lieu de nombre
            'Prix Unitaire': [100.0],
            'Catégorie': ['Meubles']
        }
        pd.DataFrame(invalid_data).to_csv(self.new_data_file, index=False, encoding='utf-8')

        importer = ImportCSV(self.new_data_file, self.database_file)

        with self.assertRaises(ColumnTypeError):
            importer.merge_data()

    def test_empty_cells(self):
        # Fichier CSV avec des cellules vides
        invalid_data = {
            'Nom du Produit': ['Armoire'],
            'Quantité': [None],  # Cellule vide
            'Prix Unitaire': [100.0],
            'Catégorie': ['Meubles']
        }
        pd.DataFrame(invalid_data).to_csv(self.new_data_file, index=False, encoding='utf-8')

        importer = ImportCSV(self.new_data_file, self.database_file)

        with self.assertRaises(EmptyCellError):
            importer.merge_data()

    def test_merge_with_duplicates(self):
        # Données avec doublons
        new_data = {
            'Nom du Produit': ['Chaise'],
            'Quantité': [5],
            'Prix Unitaire': [20.0],
            'Catégorie': ['Meubles']
        }
        pd.DataFrame(new_data).to_csv(self.new_data_file, index=False, encoding='utf-8')

        importer = ImportCSV(self.new_data_file, self.database_file)
        importer.merge_data()

        # Vérifier les résultats
        updated_data = pd.read_csv(self.database_file, encoding='utf-8')
        chaise = updated_data[updated_data['Nom du Produit'] == 'Chaise']
        self.assertEqual(len(chaise), 1)  # Doublons fusionnés
        self.assertEqual(chaise['Quantité'].iloc[0], 15)  # Quantité additionnée

if __name__ == '__main__':
    unittest.main()
