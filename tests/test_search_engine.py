import unittest
import pandas as pd
import os
from stock_manager.search_engine import SearchEngine

class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        # Fichier CSV de test
        self.test_file = "test_search.csv"

        # Données de test
        test_data = {
            'Nom du Produit': ['Chaise', 'Table', 'Armoire', 'Chaise longue'],
            'Quantité': [10, 5, 3, 7],
            'Prix Unitaire': [20.0, 50.0, 100.0, 150.0],
            'Catégorie': ['Meubles', 'Meubles', 'Meubles', 'Extérieur']
        }
        pd.DataFrame(test_data).to_csv(self.test_file, index=False, encoding='utf-8')

    def tearDown(self):
        # Supprimer le fichier CSV de test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_search_by_name(self):
        engine = SearchEngine(self.test_file)

        # Recherche par nom
        result = engine.search(name="Chaise")
        self.assertEqual(len(result), 2)  # "Chaise" et "Chaise longue" correspondent
        self.assertIn("Chaise", result['Nom du Produit'].values)
        self.assertIn("Chaise longue", result['Nom du Produit'].values)

    def test_search_by_category(self):
        engine = SearchEngine(self.test_file)

        # Recherche par catégorie
        result = engine.search(category="Meubles")
        self.assertEqual(len(result), 3)  # Chaise, Table, Armoire
        self.assertTrue(all(result['Catégorie'] == "Meubles"))

    def test_search_by_price_range(self):
        engine = SearchEngine(self.test_file)

        # Recherche par plage de prix
        result = engine.search(price_range=(20, 100))
        self.assertEqual(len(result), 3)  # Chaise, Table, Armoire
        self.assertTrue((result['Prix Unitaire'] >= 20).all())
        self.assertTrue((result['Prix Unitaire'] <= 100).all())

    def test_search_combined_filters(self):
        engine = SearchEngine(self.test_file)

        # Recherche avec plusieurs filtres
        result = engine.search(name="Chaise", category="Meubles", price_range=(10, 50))
        self.assertEqual(len(result), 1)  # Seule "Chaise" correspond
        self.assertEqual(result.iloc[0]['Nom du Produit'], "Chaise")

    def test_no_match(self):
        engine = SearchEngine(self.test_file)

        # Aucun résultat
        result = engine.search(name="Canapé")
        self.assertEqual(len(result), 0)  # Aucun produit ne correspond

if __name__ == '__main__':
    unittest.main()
