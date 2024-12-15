from stock_manager import ImportCSV, SearchEngine, ReportGenerator
import argparse
from pathlib import Path
import re


def csv_file_validator(file_path):
    path = Path(file_path)
    arg_error = argparse.ArgumentTypeError

    if not path.exists():
        raise arg_error(f"The file '{file_path}' does not exist.")

    if not path.is_file():
        raise arg_error(f"'{file_path}' is not a valid file.")

    if path.suffix.lower() != ".csv":
        raise arg_error(f"'{file_path}' does not have the '.csv' extension.")

    return path


def parse_parameters(input_string):
    parameters = {
        "name": None,
        "category": None,
        "price_range": None
    }

    # Expressions régulières ajustées pour chaque paramètre
    name_match = re.search(r'\bname=([^ ]+)', input_string)
    category_match = re.search(r'\bcategory=([^ ]+)', input_string)
    price_range_match = re.search(r'price_range=\((\d+),(\d+)\)', input_string)

    # Extraire et ajouter les paramètres au dictionnaire
    if name_match:
        parameters['name'] = name_match.group(1)
    if category_match:
        parameters['category'] = category_match.group(1)
    if price_range_match:
        min_price = int(price_range_match.group(1))
        max_price = int(price_range_match.group(2))
        parameters['price_range'] = (min_price, max_price)

    return parameters


def main(my_args):
    db = my_args.data_base

    if my_args.import_csv:
        csv_to_merge = my_args.import_csv
        try:
            ImportCSV(csv_to_merge, db).merge_data()
        except ImportError as e:
            print('Merge error:', e)

    if my_args.search:
        engine = SearchEngine(db)
        result = parse_parameters(my_args.search)
        filtered_data = engine.search(
            name=result['name'],
            category=result['category'],
            price_range=result['price_range'])
        print(filtered_data)

    if my_args.report:
        ReportGenerator(db).save_report(my_args.report)


if __name__ == '__main__':
    search_ex = 'name=Chaise category=Meubles price_range=(10,50)'

    parser = argparse.ArgumentParser(description='Stocks manager.')
    parser.add_argument('data_base',
                        type=csv_file_validator,
                        help='The main csv file that contains your data.')
    parser.add_argument('-i', '--import_csv',
                        type=csv_file_validator,
                        help='Import CSV file.')
    parser.add_argument('-s', '--search',
                        help=f"Search in the inventory. Syntax: '{search_ex}'")
    parser.add_argument('-r', '--report',
                        type=csv_file_validator,
                        help='Create a report in the specified file.')
    args = parser.parse_args()

    main(args)
