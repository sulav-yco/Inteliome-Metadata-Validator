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
        
        sql_keywords = {
            "ADD", "ALL", "ALLOCATE", "ALTER", "AND", "ANY", "ARE", "ARRAY", "AS", "ASENSITIVE", "ASYMMETRIC", "AT",
            "ATOMIC", "AUTHORIZATION", "BEGIN", "BETWEEN", "BIGINT", "BINARY", "BLOB", "BOOLEAN", "BOTH", "BY", "CALL",
            "CALLED", "CASCADED", "CASE", "CAST", "CHAR", "CHARACTER", "CHECK", "CLOB", "CLOSE", "COLLATE", "COLUMN",
            "COMMIT", "CONNECT", "CONSTRAINT", "CONTINUE", "CORRESPONDING", "CREATE", "CROSS", "CUBE", "CURRENT",
            "CURRENT_DATE", "CURRENT_DEFAULT_TRANSFORM_GROUP", "CURRENT_PATH", "CURRENT_ROLE", "CURRENT_TIME",
            "CURRENT_TIMESTAMP", "CURRENT_TRANSFORM_GROUP_FOR_TYPE", "CURRENT_USER", "CURSOR", "CYCLE", "DATE", "DAY",
            "DEALLOCATE", "DEC", "DECIMAL", "DECLARE", "DEFAULT", "DELETE", "DEREF", "DESCRIBE", "DETERMINISTIC",
            "DISCONNECT", "DISTINCT", "DO", "DOUBLE", "DROP", "DYNAMIC", "EACH", "ELEMENT", "ELSE", "END", "END-EXEC",
            "ESCAPE", "EXCEPT", "EXEC", "EXECUTE", "EXISTS", "EXIT", "EXTERNAL", "FALSE", "FETCH", "FILTER", "FLOAT",
            "FOR", "FOREIGN", "FREE", "FROM", "FULL", "FUNCTION", "GET", "GLOBAL", "GRANT", "GROUP", "GROUPING", "HAVING",
            "HOLD", "HOUR", "IDENTITY", "IF", "IMMEDIATE", "IN", "INDICATOR", "INNER", "INOUT", "INPUT", "INSENSITIVE",
            "INSERT", "INT", "INTEGER", "INTERSECT", "INTERVAL", "INTO", "IS", "ISOLATION", "JOIN", "LANGUAGE", "LARGE",
            "LATERAL", "LEADING", "LEAVE", "LEFT", "LIKE", "LOCAL", "LOCALTIME", "LOCALTIMESTAMP", "LOOP", "MATCH",
            "MEMBER", "MERGE", "METHOD", "MINUTE", "MODIFIES", "MODULE", "MONTH", "MULTISET", "NATIONAL", "NATURAL",
            "NCHAR", "NCLOB", "NEW", "NO", "NONE", "NOT", "NULL", "NUMERIC", "OF", "OLD", "ON", "ONLY", "OPEN", "OR",
            "ORDER", "OUT", "OUTER", "OUTPUT", "OVER", "OVERLAPS", "PARAMETER", "PARTITION", "PRECISION", "PREPARE",
            "PRIMARY", "PROCEDURE", "RANGE", "READS", "REAL", "RECURSIVE", "REF", "REFERENCES", "REFERENCING",
            "REGR_AVGX", "REGR_AVGY", "REGR_COUNT", "REGR_INTERCEPT", "REGR_R2", "REGR_SLOPE", "REGR_SXX", "REGR_SXY",
            "REGR_SYY", "RELEASE", "REPEAT", "RESIGNAL", "RESULT", "RETURN", "RETURNS", "REVOKE", "RIGHT", "ROLLBACK",
            "ROLLUP", "ROW", "ROWS", "SAVEPOINT", "SCOPE", "SCROLL", "SEARCH", "SECOND", "SELECT", "SENSITIVE",
            "SESSION_USER", "SET", "SIGNAL", "SIMILAR", "SMALLINT", "SOME", "SPECIFIC", "SPECIFICTYPE", "SQL",
            "SQLEXCEPTION", "SQLSTATE", "SQLWARNING", "START", "STATIC", "SUBMULTISET", "SYMMETRIC", "SYSTEM",
            "SYSTEM_USER", "TABLE", "THEN", "TIME", "TIMESTAMP", "TIMEZONE_HOUR", "TIMEZONE_MINUTE", "TO", "TRAILING",
            "TRANSLATION", "TREAT", "TRIGGER", "TRUE", "UNDO", "UNION", "UNIQUE", "UNKNOWN", "UNNEST", "UPDATE", "USER",
            "USING", "VALUE", "VALUES", "VARCHAR", "VARYING", "WHEN", "WHENEVER", "WHERE", "WHILE", "WINDOW", "WITH",
            "WITHIN", "WITHOUT", "YEAR", "COUNT", "AVG"
                }


        column_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
        
        tokens = column_pattern.findall(sql_query)
        columns = [token for token in tokens if token.upper() not in sql_keywords]
        return columns
        
        
        
        
    def validate_semantics(self, generated_semantics: Dict):
        
        key = list(generated_semantics.keys())[0]
        generated_semantics = generated_semantics.get(key)
        
        schema_dict = self.parse_schema()
        attributes = generated_semantics["attributes"]
        metrics = generated_semantics["metrics"]

        attribute_keys = list(attributes.keys())
        metrics_keys = list(metrics.keys())
        
        reference_columns = attribute_keys + metrics_keys + schema_dict["column_ids"]
        
        for key,values in attributes.items():
                          
            if "include" in values and values["include"]:
                include_list = values["include"]
                for include in include_list:
                    if include not in reference_columns:
                        raise ValueError(f"Incorrect reference {include} in the include list. Not found in schema")
                               
            if "calculation" in values and values["calculation"]:
                calculation = values["calculation"]
                column_names = self.extract_column_names(calculation)
                
                for column in column_names:
                    if column not in schema_dict["column_ids"]:
                        raise ValueError(f"Incorrect reference {column} used in the calculation in attribute {key}. No such column found in schema")

        for key,values in metrics.items():
            if "calculation" in values and values["calculation"]:        
                calculation = values["calculation"]
                column_names = self.extract_column_names(calculation)
                
                for column in column_names:
                    if column not in reference_columns:
                        raise ValueError(f"Incorrect reference {column} used in the calculation in metric {key}. No such column found in schema")
                        
        print("End of Semantics Validation")