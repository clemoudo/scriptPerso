import argparse
import os
from stock_manager.stock_manager import *

def main():
    parser = argparse.ArgumentParser(description="Gestion de stocks via ligne de commande.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Sous-commande : consolidate
    parser_consolidate = subparsers.add_parser("consolidate", help="Consolider les fichiers CSV dans une base unique.")
    parser_consolidate.add_argument("--input-dir", required=True, help="Répertoire contenant les fichiers CSV à consolider.")

    # Sous-commande : search
    parser_search = subparsers.add_parser("search", help="Rechercher des produits dans la base de données.")
    parser_search.add_argument("--name", help="Nom du produit à rechercher.")
    parser_search.add_argument("--category", help="Catégorie du produit.")
    parser_search.add_argument("--min-price", type=float, help="Prix minimum.")
    parser_search.add_argument("--max-price", type=float, help="Prix maximum.")
    parser_search.add_argument("--min-quantity", type=int, help="Quantité minimale en stock.")

    # Sous-commande : report
    parser_report = subparsers.add_parser("report", help="Générer un rapport à partir des données consolidées.")
    parser_report.add_argument("--type", required=True, choices=["summary", "critical"], help="Type de rapport à générer.")
    parser_report.add_argument("--format", required=True, choices=["csv", "json", "txt"], help="Format du rapport généré.")
    parser_report.add_argument("--output", required=True, help="Chemin de sortie du rapport.")

    args = parser.parse_args()

    # Initialisation du gestionnaire de stocks
    db_path = "stocks.sqlite"
    manager = StockManager(db_path)

    try:
        if args.command == "consolidate":
            # Commande : Consolidation des fichiers CSV
            if not os.path.isdir(args.input_dir):
                print(f"Erreur : Le répertoire {args.input_dir} n'existe pas.")
                return
            manager.initialize_database()
            manager.consolidate_files(args.input_dir)
            print("Consolidation terminée avec succès.")

        elif args.command == "search":
            # Commande : Recherche de produits
            criteria = {}
            if args.name:
                criteria["name"] = args.name
            if args.category:
                criteria["category"] = args.category
            if args.min_price is not None:
                criteria["unit_price >="] = args.min_price
            if args.max_price is not None:
                criteria["unit_price <="] = args.max_price
            if args.min_quantity is not None:
                criteria["quantity >="] = args.min_quantity

            results = manager.search_products(criteria)
            print("Résultats de recherche :")
            print(results)

        elif args.command == "report":
            # Commande : Génération de rapports
            manager.generate_report(args.type, args.output, args.format)
            print(f"Rapport généré avec succès : {args.output}")

    finally:
        manager.close()
