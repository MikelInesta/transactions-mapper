from typing import Dict, List, Optional
import re
from pydantic import BaseModel

class MappingRule(BaseModel):
    """A rule for mapping payee names."""
    pattern: str
    replacement: str
    description: Optional[str] = None

class PayeeMapper:
    """Handles the mapping of payee names using regex patterns."""
    
    def __init__(self, mappings: List[MappingRule]):
        self.mappings = mappings
        self._compiled_patterns = [
            (re.compile(rule.pattern, re.IGNORECASE), rule.replacement)
            for rule in mappings
        ]
    
    def map_payee(self, payee_name: str) -> str:
        """
        Apply all mapping rules to a payee name.
        
        Args:
            payee_name: The original payee name from the transaction
            
        Returns:
            The standardized payee name
        """
        result = payee_name
        for pattern, replacement in self._compiled_patterns:
            result = pattern.sub(replacement, result)
        return result.strip()
    
    @classmethod
    def from_yaml(cls, yaml_content: str) -> 'PayeeMapper':
        """
        Create a PayeeMapper instance from YAML content.
        
        Args:
            yaml_content: YAML string containing mapping rules
            
        Returns:
            A configured PayeeMapper instance
        """
        import yaml
        data = yaml.safe_load(yaml_content)
        mappings = [MappingRule(**rule) for rule in data.get('mappings', [])]
        return cls(mappings) 