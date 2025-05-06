from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
from .mapper import PayeeMapper

class TransactionProcessor:
    """Processes transaction files and applies mappings."""
    
    def __init__(self, mapper: PayeeMapper):
        self.mapper = mapper
    
    def process_file(self, input_path: Path, output_path: Path, 
                    payee_column: str = 'payee',
                    date_column: Optional[str] = None,
                    amount_column: Optional[str] = None) -> None:
        """
        Process a transaction file and save the standardized version.
        
        Args:
            input_path: Path to the input file (Excel or CSV)
            output_path: Path where to save the processed file
            payee_column: Name of the column containing payee information
            date_column: Name of the date column (optional)
            amount_column: Name of the amount column (optional)
        """
        # Read the input file
        if input_path.suffix.lower() == '.xlsx':
            df = pd.read_excel(input_path)
        else:
            df = pd.read_csv(input_path)
        
        # Apply mappings to payee column
        if payee_column in df.columns:
            df[payee_column] = df[payee_column].apply(self.mapper.map_payee)
        
        # Save the processed file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
    
    @classmethod
    def from_mapping_file(cls, mapping_path: Path) -> 'TransactionProcessor':
        """
        Create a TransactionProcessor instance from a mapping file.
        
        Args:
            mapping_path: Path to the YAML mapping file
            
        Returns:
            A configured TransactionProcessor instance
        """
        mapper = PayeeMapper.from_yaml(mapping_path.read_text())
        return cls(mapper) 