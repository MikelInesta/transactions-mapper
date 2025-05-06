# Transactions Mapper

A tool to standardize and normalize transaction data before importing it into financial management systems like Firefly-III.

## Features

- Convert Excel/CSV transaction files to standardized format
- Apply custom mappings to normalize payee names
- Interactive mapping generation from transaction files
- Handle unclean Excel files with headers, images, and extra data
- Specify custom column names for different data sources
- Separate mapping configuration from the application
- Extensible architecture for future enhancements

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Processing Transaction Files

1. Create a mappings file (YAML format) with your payee name mappings
2. Run the application:
   ```bash
   python -m transactions_mapper process --input transactions.xlsx --mappings mappings.yaml --output standardized.csv
   ```

### Generating Mappings

You can interactively generate mappings from your transaction files:

```bash
# Generate new mappings
python -m transactions_mapper generate-mappings input.xlsx mappings.yaml --payee-column "CONCEPTO"

# Extend existing mappings
python -m transactions_mapper generate-mappings input.xlsx new_mappings.yaml --payee-column "CONCEPTO" --existing-mappings current_mappings.yaml
```

The generator will:
1. Read your transaction file
2. Show each unique payee name
3. Ask you to provide a standardized name for each
4. Optionally add a description
5. Save all mappings to the specified YAML file

You can press Ctrl+C at any time to save the current mappings and exit.

### Handling Different File Formats

The tool supports various input file formats and can handle unclean data:

```bash
# Basic usage
python -m transactions_mapper process input.xlsx mappings.yaml output.csv

# Skip rows at the beginning (e.g., for files with headers or images)
python -m transactions_mapper process input.xlsx mappings.yaml output.csv --skip-rows 5

# Specify custom column names
python -m transactions_mapper process input.xlsx mappings.yaml output.csv --payee-column "CONCEPTO" --date-column "FECHA" --amount-column "IMPORTE"

# Disable automatic data cleaning
python -m transactions_mapper process input.xlsx mappings.yaml output.csv --no-clean-data
```

### Column Mapping

You can specify the names of your source columns to map them to the standardized format:

- `--payee-column`: Name of the column containing payee/description information (default: "payee")
- `--date-column`: Name of the column containing transaction dates
- `--amount-column`: Name of the column containing transaction amounts

For example, if your Excel file uses "CONCEPTO" for the description column:
```bash
python -m transactions_mapper process input.xlsx mappings.yaml output.csv --payee-column "CONCEPTO"
```

### Data Cleaning

The tool automatically cleans your data by:
- Removing empty rows and columns
- Skipping specified number of rows at the beginning
- Standardizing column names

You can disable automatic cleaning with `--no-clean-data` if needed.

## Project Structure

```
transactions_mapper/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── processor.py
│   │   └── mapper.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── cli.py
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## License

MIT 