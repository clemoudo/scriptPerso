from cgi import parse

from stock_manager import ImportCSV, SearchEngine, ReportGenerator
import argparse


def main():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_base', help='The main csv file that contains your data.')
    parser.add_argument('-i', '--import_csv', help='Import CSV file.')
    parser.add_argument('-s', '--search', nargs='+', help='Do a research in the data base.')
    parser.add_argument('-r', '--report', help='Create a report in the specified file.')
    args = parser.parse_args()

    if args.search and len(args.search) > 3:
        parser.error("The --search option can maximum have three values.")

    main()
