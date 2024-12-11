import pandas as pd

class ReportGenerator:
    def __init__(self, data):
        """ Initialise le générateur de rapports avec un DataFrame contenant les données consolidées.
        PRE :
        - data doit être un DataFrame pandas non vide.

        POST :
        - Une instance de ReportGenerator est initialisée avec les données fournies.

        RAISE :
        - ValueError si data est vide ou n'est pas un DataFrame.
        """
        if not isinstance(data, pd.DataFrame) or data.empty:
            raise ValueError("Les données doivent être un DataFrame pandas non vide.")
        self.data = data

    def calculate_total_stock_value(self):
        """ Calcule la valeur totale des stocks (quantité * prix unitaire).

        PRE :
        - Les colonnes 'quantity' et 'unit_price' doivent exister dans self.data.

        POST :
        - Retourne la valeur totale des stocks sous forme de float.

        RAISE :
        - KeyError si l'une des colonnes requises est manquante.
        """
        if 'quantity' not in self.data.columns or 'unit_price' not in self.data.columns:
            raise KeyError("Les colonnes 'quantity' et 'unit_price' sont requises pour calculer la valeur totale des stocks.")

        total_value = (self.data['quantity'] * self.data['unit_price']).sum()
        return total_value

    def count_products_by_category(self):
        """ Compte le nombre de produits par catégorie.

        PRE :
        - La colonne 'category' doit exister dans self.data.

        POST :
        - Retourne un dictionnaire avec les catégories comme clés et le nombre de produits comme valeurs.

        RAISE :
        - KeyError si la colonne 'category' est manquante.
        """
        if 'category' not in self.data.columns:
            raise KeyError("La colonne 'category' est requise pour compter les produits par catégorie.")

        counts = self.data['category'].value_counts().to_dict()
        return counts

    def identify_critical_stock(self, threshold=10):
        """ Identifie les produits en stock critique (quantité < threshold).

        PRE :
        - La colonne 'quantity' doit exister dans self.data.
        - threshold doit être un entier positif.

        POST :
        - Retourne un DataFrame contenant les produits en stock critique.

        RAISE :
        - KeyError si la colonne 'quantity' est manquante.
        - ValueError si threshold est négatif.
        """
        if 'quantity' not in self.data.columns:
            raise KeyError("La colonne 'quantity' est requise pour identifier les stocks critiques.")
        if threshold < 0:
            raise ValueError("Le seuil de stock critique (threshold) doit être un entier positif.")

        critical_stock = self.data[self.data['quantity'] < threshold]
        return critical_stock

    def export_report(self, report_data, file_path, file_format="csv"):
        """ Exporte les données du rapport dans le format spécifié.

        PRE :
        - report_data doit être un DataFrame pandas.
        - file_path doit être un chemin valide.
        - file_format doit être l'un des suivants : 'csv', 'json', 'txt'.

        POST :
        - Le fichier est exporté au chemin spécifié dans le format choisi.

        RAISE :
        - ValueError si file_format n'est pas pris en charge.
        - OSError si l'écriture du fichier échoue.
        """
        if not isinstance(report_data, pd.DataFrame):
            raise ValueError("Les données du rapport doivent être un DataFrame pandas.")
        if file_format not in ["csv", "json", "txt"]:
            raise ValueError(f"Format non pris en charge : {file_format}. Formats supportés : csv, json, txt.")

        try:
            if file_format == "csv":
                report_data.to_csv(file_path, index=False)
            elif file_format == "json":
                report_data.to_json(file_path, orient="records", lines=True)
            elif file_format == "txt":
                with open(file_path, "w") as f:
                    f.write(report_data.to_string(index=False))
        except Exception as e:
            raise OSError(f"Erreur lors de l'écriture du fichier : {e}")
