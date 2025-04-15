from validator.base_validator import BaseValidator

class SchemaValidator(BaseValidator):
    def __init__(self):
        super().__init__()
        
    # def validate(self, schema, ddl):
    def validate(self, schema):
        
        self.validate_format(schema)
        # self.validate_ddl(schema, ddl)
        
    
    def validate_ddl(self, schema, ddl):
        parsed_ddl = self.parse_ddl(ddl)
        ...
        
        
    def validate_format(self, schema):
        schema = schema.get("GeneratedSchema")
        required_keys_dict = {
            "subject_area": str,
            "table_info":   list,
            "columns":      dict,
        }
        self.check_primary_keys(schema, required_keys_dict = required_keys_dict)
        for table in schema.get("table_info"):
            self.check_table_info(table)
        self.check_columns(schema.get("columns"))
        # self.check_indentation(schema)   
        
    def check_primary_keys(self,schema,required_keys_dict:dict):
        self.check_required_keys(schema.keys(),required_keys=list(required_keys_dict.keys()))
        for key in schema.keys():
            # required_key_type = required_keys_dict.get(key)
            self.check_instance(schema.get(key), required_keys_dict.get(key))
            
            
    def check_table_info(self, ind_table_info):
        
        self.check_instance(ind_table_info, dict)
        print("Ind table")
        required_keys = {
            "table" : str,
            "joins" : list
        }    
        self.check_required_keys(ind_table_info, required_keys=list(required_keys.keys()))
        for key in ind_table_info:
            print(ind_table_info.get(key))
            self.check_instance(ind_table_info.get(key), required_keys.get(key))
          
          
        
    def check_columns(self,columns):
        for column_name in columns:
            self.check_instance(columns.get(column_name), dict)
            self.check_column(columns.get(column_name))
            
            
            
        
    def check_column(self,column):
        required_keys = {
            "name": str,
            "type": str,
            "column": str,
            "desc": str,
            "primary_key": bool,
            "foreign_key": bool,
            # "fetch": bool
        }
        
        self.check_required_keys(column, required_keys=list(required_keys.keys()))
        print("RIGHTTTT")
        for key in column:
            print(key)
            self.check_instance(column.get(key), required_keys.get(key))       
        


    # def check_indentation(self,schema):
    #     ...
    
    def parse_ddl(self,ddl) -> dict:
        ...
        