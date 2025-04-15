import yaml
from typing import List, Dict
from pyvalidator.schema_validator import GeneratedSchema
from simple_ddl_parser import DDLParser



def parse_ddl_to_metadata(ddl:str):
    return DDLParser(ddl).run(output_mode="hql")




class DDLValidator():
    
    def __init__(self, ddls = None):
        self.ddl = parse_ddl_to_metadata(ddls)
        
        
    def validate_schema(self, schema: GeneratedSchema):
        schema = schema.values()
        # check table_name
        if schema.table_info[0].table != self.ddl["table_name"]:
            raise ValueError(f"{schema.table_info[0].table} table name not in DDL")
        
        schema_columns = {col.name.upper(): col for col in schema.columns.values()}  # upper for case-insensitivity

        # Step 3: Validate DDL columns against schema
        for ddl_col in self.ddl[0]['columns']:
            ddl_col_name = ddl_col['name'].upper()
            ddl_col_type = ddl_col['type'].upper()
            ddl_col_primary_key = ddl_col["primary_key"].upper()
            
            
            
            

            if ddl_col_name not in schema_columns:
                raise ValueError(f"DDL column '{ddl_col_name}' not found in schema.")

            schema_col_type = schema_columns[ddl_col_name].type.upper()
            if ddl_col_type != schema_col_type:
                raise ValueError(f"Type mismatch for column '{ddl_col_name}': DDL type '{ddl_col_type}', Schema type '{schema_col_type}'.")

        print("Schema successfully validated against DDL.")
                
                
        
        
