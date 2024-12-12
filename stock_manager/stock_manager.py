from data_consolidator import DataConsolidator
from database_manager import DatabaseManager
from report_generator import ReportGenerator
import pandas as pd

class StockManager:
    def __init__(self, db_path):
        """  Initialise le gestionnaire central des stocks avec tous les modules nécessaires.
        PRE :
        - db_path est une chaîne valide représentant le chemin de la base SQLite.

        POST :
        - Tous les sous-modules sont initialisés et prêts à être utilisés.

        RAISE :
        - ValueError si db_path est invalide.
        """
        self.db_manager = DatabaseManager(db_path)
        self.data_consolidator = DataConsolidator()
        self.report_generator = None  # Initialisé après consolidation

    def initialize_database(self):
        """ Initialise la base de données en créant les tables nécessaires.

        PRE :
        - La connexion à la base SQLite doit être active.

        POST :
        - La table 'stocks' est créée dans la base de données.
        """
        self.db_manager.create_table()

    def consolidate_files(self, input_dir):
        """ Consolide les fichiers CSV d'un répertoire en une base unique et insère les données dans la base SQLite.

        PRE :
        - input_dir est une chaîne valide représentant le chemin d'un répertoire contenant des fichiers CSV.

        POST :
        - Les données consolidées sont insérées dans la base SQLite.

        RAISE :
        - FileNotFoundError si le répertoire est invalide ou inexistant.
        """
        self.data_consolidator.load_csv_files(input_dir)
        self.data_consolidator.clean_data()
        self.data_consolidator.remove_duplicates()
        consolidated_data = self.data_consolidator.get_data()
        self.db_manager.insert_data(consolidated_data)
        self.report_generator = ReportGenerator(consolidated_data)

    def search_products(self, criteria):
        """ Effectue une recherche multicritères dans la base de données des stocks.

        PRE :
        - criteria est un dictionnaire avec des clés valides comme 'name', 'category', 'quantity', ou 'unit_price'.

        POST :
        - Retourne un DataFrame avec les produits correspondant aux critères.

        RAISE :
        - Error si la requête échoue.
        """
        return self.db_manager.query_data(criteria)

    def generate_report(self, report_type, export_path, export_format):
        """ Génère un rapport et l'exporte dans le format spécifié.

        PRE :
        - report_type est une chaîne valide parmi ['summary', 'critical'].
        - export_path est un chemin valide pour l'exportation du fichier.
        - export_format est une chaîne valide parmi ['csv', 'json', 'txt'].

        POST :
        - Le rapport est généré et exporté dans le format spécifié.

        RAISE :
        - ValueError si les paramètres sont invalides.
        - OSError si l'écriture du fichier échoue.
        """
        if not self.report_generator:
            raise ValueError("Les données consolidées doivent être disponibles pour générer un rapport.")

        if report_type == "summary":
            report_data = pd.DataFrame({
                "Total Stock Value": [self.report_generator.calculate_total_stock_value()],
                "Products by Category": [self.report_generator.count_products_by_category()]
            })
        elif report_type == "critical":
            report_data = self.report_generator.identify_critical_stock()
        else:
            raise ValueError("Type de rapport invalide. Utilisez 'summary' ou 'critical'.")

        self.report_generator.export_report(report_data, export_path, file_format=export_format)

    def close(self):
        """ Ferme proprement toutes les connexions et libère les ressources utilisées.

        PRE :
        - Les modules utilisent des connexions actives à des ressources comme des bases de données.

        POST :
        - Toutes les connexions sont fermées proprement.
        """
        self.db_manager.close_connection()
