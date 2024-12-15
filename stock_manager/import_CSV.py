import pandas as pd


class ColumnNameError(ImportError):
    pass

class ColumnTypeError(ImportError):
    pass

class EmptyCellError(ImportError):
    pass

class ImportCSV:
    def __init__(self, csv_file, data_base):
        self.csv_file = pd.read_csv(csv_file, encoding='utf-8')
        self.data_base = pd.read_csv(data_base, encoding='utf-8')
        self.data_base_address = data_base

    def _validity_check(self):
        if self.csv_file.columns.tolist() != self.data_base.columns.tolist(): # ['Nom du Produit', 'Quantité', 'Prix Unitaire', 'Catégorie']
            raise ColumnNameError("Column names do not match.")
        if self.csv_file.dtypes.tolist() != self.data_base.dtypes.tolist():  # [dtype('O'), dtype('int64'), dtype('float64'), dtype('O')]
            raise ColumnTypeError("Column types do not match.")
        if self.csv_file.isnull().values.any():
            raise EmptyCellError("Empty cells found.")

    def merge_data(self):
        self._validity_check()
        data_merged = pd.concat([self.data_base, self.csv_file])
        column_order = self.data_base.columns.tolist()
        data_grouped =data_merged.groupby(['Nom du Produit', 'Catégorie'], as_index=False).agg({
            'Quantité': 'sum',
            'Prix Unitaire': 'first'  # Garde le premier prix unitaire trouvé
        })
        data_final = data_grouped[column_order]
        data_final.to_csv(self.data_base_address, index=False, encoding='utf-8')
