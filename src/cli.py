import click
from pathlib import Path
from .core.processor import TransactionProcessor
from .core.mapper import PayeeMapper, MappingRule
import yaml
import pandas as pd

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
@click.option('--skip-rows', type=int, default=0, help='Number of rows to skip at the beginning of the file')
@click.option('--no-clean-data', is_flag=True, help='Disable automatic data cleaning')
def process(input_file: str, mapping_file: str, output_file: str,
           payee_column: str, date_column: str, amount_column: str,
           skip_rows: int, no_clean_data: bool):
    """Process a transaction file using the provided mappings."""
    try:
        processor = TransactionProcessor.from_mapping_file(Path(mapping_file))
        processor.process_file(
            input_path=Path(input_file),
            output_path=Path(output_file),
            payee_column=payee_column,
            date_column=date_column,
            amount_column=amount_column,
            skip_rows=skip_rows,
            clean_data=not no_clean_data
        )
        click.echo(f"Successfully processed {input_file} -> {output_file}")
    except Exception as e:
        click.echo(f"Error processing file: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_mapping_file', type=click.Path())
@click.option('--payee-column', default='payee', help='Name of the payee column')
@click.option('--skip-rows', type=int, default=0, help='Number of rows to skip at the beginning of the file')
@click.option('--existing-mappings', type=click.Path(exists=True), help='Path to existing mappings file to extend')
def generate_mappings(input_file: str, output_mapping_file: str, payee_column: str, 
                     skip_rows: int, existing_mappings: str):
    """Interactively generate mappings from a transaction file."""
    try:
        # Load existing mappings if provided
        existing_rules = []
        if existing_mappings:
            with open(existing_mappings, 'r') as f:
                data = yaml.safe_load(f)
                existing_rules = [MappingRule(**rule) for rule in data.get('mappings', [])]
        
        # Read the input file
        input_path = Path(input_file)
        if '.xls' in input_path.suffix.lower():
            df = pd.read_excel(input_path, skiprows=skip_rows)
        else:
            df = pd.read_csv(input_path, skiprows=skip_rows)
        
        if payee_column not in df.columns:
            raise click.ClickException(f"Column '{payee_column}' not found in the input file")
        
        # Get unique payee values
        unique_payees = df[payee_column].dropna().unique()
        
        # Create a temporary mapper with existing rules
        mapper = PayeeMapper(existing_rules)
        new_rules = []
        
        click.echo("\nStarting interactive mapping generation...")
        click.echo("For each unique payee, you'll be asked to provide a standardized name.")
        click.echo("Press Ctrl+C at any time to save the current mappings and exit.\n")
        
        for payee in unique_payees:
            # Skip if already mapped
            mapped = mapper.map_payee(payee)
            if mapped != payee:
                click.echo(f"Already mapped: {payee} -> {mapped}")
                continue
            
            click.echo(f"\nPayee: {payee}")
            replacement = click.prompt("Enter standardized name (or press Enter to skip)", default="")
            
            if replacement:
                description = click.prompt("Enter description (optional)", default="")
                new_rule = MappingRule(
                    pattern=payee,
                    replacement=replacement,
                    description=description if description else None
                )
                new_rules.append(new_rule)
                click.echo(f"Added mapping: {payee} -> {replacement}")
        
        # Combine existing and new rules
        all_rules = existing_rules + new_rules
        
        # Save mappings
        output_path = Path(output_mapping_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump({'mappings': [rule.dict() for rule in all_rules]}, f, sort_keys=False)
        
        click.echo(f"\nMappings saved to {output_mapping_file}")
        
    except KeyboardInterrupt:
        # Save current mappings on Ctrl+C
        if new_rules:
            all_rules = existing_rules + new_rules
            output_path = Path(output_mapping_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                yaml.dump({'mappings': [rule.dict() for rule in all_rules]}, f, sort_keys=False)
            
            click.echo(f"\nMappings saved to {output_mapping_file}")
    except Exception as e:
        click.echo(f"Error generating mappings: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli() 