# Stock Manager

## Description

The **Stock Manager** program is a Python-based command-line tool to manage inventory efficiently. It allows you to:

- Import and merge inventory data from CSV files.
- Search for specific products by name, category, or price range.
- Generate inventory reports, including total quantities and values by category.

## Features

1. **Data Import**: Merge new inventory data into an existing database while ensuring consistency.
2. **Search**: Perform detailed searches using product name, category, or a price range.
3. **Report Generation**: Create a summary report showing total quantities and values per category and overall.

## Installation

### Prerequisites

- Python 3.7+
- The `pandas` library (for data manipulation)

### Installation Steps

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program from the command line using the following options:

### Basic Syntax

```bash
python main.py [data_base] [options]
```

### Options

- `data_base` (required): Path to the main CSV file containing your inventory data.
- `-i`, `--import_csv`: Import a new CSV file into the database.
- `-s`, `--search`: Search the inventory using syntax like:

  ```
  name=Chaise category=Meubles price_range=(10,50)
  ```

  You can use any combination of `name`, `category`, and `price_range`. Only specified filters are applied.
- `-r`, `--report`: Generate a report and save it to the specified CSV file.

### Examples

#### Import Data

```bash
python stock_manager.py database.csv -i new_stock.csv
```

#### Search Inventory

```bash
python stock_manager.py database.csv -s "name=Table category=Furniture"
```

#### Generate Report

```bash
python stock_manager.py database.csv -r inventory_report.csv
```

## CSV Format Requirements

Your CSV files must adhere to the following structure:

| Nom du Produit  | Quantité | Prix Unitaire | Catégorie   |
|-----------------|------------|---------------|--------------|
| Chaise          | 10         | 20.0          | Meubles      |
| Table           | 5          | 50.0          | Meubles      |
| ...             | ...        | ...           | ...          |

## Error Handling

The program validates input files rigorously:

- Ensures column names and types match the database.
- Detects and reports empty cells in the CSV.
- Raises errors for invalid file paths or extensions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

