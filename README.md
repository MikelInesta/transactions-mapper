# Transactions Mapper

A tool to standardize and normalize transaction data before importing it into financial management systems like Firefly-III.

## Features

- Convert Excel/CSV transaction files to standardized format
- Apply custom mappings to normalize payee names
- Separate mapping configuration from the application
- Extensible architecture for future enhancements

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a mappings file (YAML format) with your payee name mappings
2. Run the application:
   ```bash
   python -m transactions_mapper process --input transactions.xlsx --mappings mappings.yaml --output standardized.csv
   ```

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