from abc import ABC
from error.collector.error_collection import ValidationErrorCollector



class BaseValidator(ABC):
    def __init__(self):
        self.errors = []
        self.collector = ValidationErrorCollector()
        ...
    
    def validate(self, files = None):
        ...
        
    def validate_format(self, schema):
        ...
        
        
    def check_required_keys(self, keys, required_keys: list):
        for key in keys:
            if key not in required_keys:
                print(f"Key missing {key}")
            
            
    def check_instance(self, value, required_type):
        
        
        if required_type is None:
            print(f"Missing key in Schema")
            print(value)
            print(required_type)
            # return False
        
        if not isinstance(value, required_type):
            print(f"Invalid Key type {value}:\n Expected type: {required_type}\n Actual type {type(value)}")
            