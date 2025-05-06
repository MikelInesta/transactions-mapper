import click
from pathlib import Path
from .core.processor import TransactionProcessor

@click.group()
def cli():
    """Transaction Mapper - Standardize transaction data for import."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('mapping_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--payee-column', default='payee', help='Name of the payee column')
@click.option('--date-column', help='Name of the date column')
@click.option('--amount-column', help='Name of the amount column')
def process(input_file: str, mapping_file: str, output_file: str,
           payee_column: str, date_column: str, amount_column: str):
    """Process a transaction file using the provided mappings."""
    try:
        processor = TransactionProcessor.from_mapping_file(Path(mapping_file))
        processor.process_file(
            input_path=Path(input_file),
            output_path=Path(output_file),
            payee_column=payee_column,
            date_column=date_column,
            amount_column=amount_column
        )
        click.echo(f"Successfully processed {input_file} -> {output_file}")
    except Exception as e:
        click.echo(f"Error processing file: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli() 