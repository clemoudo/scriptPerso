# Importer les modules du package stock_manager
from .import_CSV import import_csv_files
from .report_generator import generate_report
from .search_engine import search_stock

# Définir les éléments exportables lors de l'import du package
__all__ = ["import_csv_files", "generate_report", "search_stock"]
