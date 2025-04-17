import re
from pyvalidator.format_validator import SemanticWrapper, GeneratedSemantics
from pprint import pprint
from typing import Dict, List


class SemanticsValidator():
    
    def __init__(self, schema = None):
        self.schema = schema
        
    
    def print_schema(self):
        pprint(self.schema)
        
        
    def parse_schema(self):

        schema_dict = dict()
        key = list(self.schema.keys())[0]
        schema = self.schema.get(key)        
        schema_dict.update({"folder": key})
        column_ids = [col for col in list(schema["columns"].keys())]
        schema_dict.update({"column_ids": column_ids})
        
        return schema_dict
            
    
    
    def extract_column_names(self, sql_query:str) -> List:
        
        pattern = re.compile(r'\[([^\[\]]+)\]')  
        tokens = pattern.findall(sql_query)
        return tokens
        
        
    def validate_references(self, references: List[str], valid_keys: List[str], context: str, key: str):
        for ref in references:
            if ref not in valid_keys:
                raise ValueError(f"Incorrect reference '{ref}' in {context} of '{key}'. Not found in schema.")



    def validate_item(self, item: Dict, schema_dict: Dict, reference_columns: List[str], section: str):
        for key, values in item.items():
            if values.get("include"):
                self.validate_references(values["include"], reference_columns, "include list", key)
            
            if values.get("calculation"):
                columns = self.extract_column_names(values["calculation"])
                self.validate_references(columns, schema_dict["column_ids"] if section == "attributes" else reference_columns, "calculation", key)

            if values.get("filter"):
                for filter_expr in values["filter"]:
                    columns = self.extract_column_names(filter_expr)
                    self.validate_references(columns, reference_columns, "filter", key)
            
    
        
    def validate_semantics(self, generated_semantics: Dict):
        key = list(generated_semantics.keys())[0]
        generated_semantics = generated_semantics.get(key)

        schema_dict = self.parse_schema()
        attributes = generated_semantics["attributes"]
        metrics = generated_semantics["metrics"]

        attribute_keys = list(attributes.keys())
        metrics_keys = list(metrics.keys())
        reference_columns = attribute_keys + metrics_keys + schema_dict["column_ids"]

        self.validate_item(attributes, schema_dict, reference_columns, "attributes")
        self.validate_item(metrics, schema_dict, reference_columns, "metrics")

        print("End of Semantics Validation")
