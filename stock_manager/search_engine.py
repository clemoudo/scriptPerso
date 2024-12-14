import pandas as pd


class SearchEngine:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def search(self, name=None, category=None, price_range=None):
        filtered_data = self.data

        if name:
            filtered_data = filtered_data[filtered_data['Produit'].str.contains(name, case=False, na=False)]

        if category:
            filtered_data = filtered_data[filtered_data['Catégorie'].str.contains(category, case=False, na=False)]

        if price_range:
            min_price, max_price = price_range
            filtered_data = filtered_data[(filtered_data['Prix Unitaire'] >= min_price) & (filtered_data['Prix Unitaire'] <= max_price)]

        return filtered_data
