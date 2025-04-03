import json
from typing import List, Dict

from src.flemmings_classes import QuestionAnswerMapping, TableMapping, ColumnMapping, MappingDB



def load_dev_mappings(file_path: str) -> List[QuestionAnswerMapping]:
    """
    Load the dev.json file and create a list of QuestionAnswerMapping objects.

    The JSON file is expected to be a list of dictionaries with the following keys:
        - 'db_id'
        - 'SpiderQuestion'
        - 'SpiderSynQuestion'
        - 'query'

    Args:
        file_path (str): Path to the dev.json file.

    Returns:
        List[QuestionAnswerMapping]: A list of QuestionAnswerMapping objects.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    qa_mappings: List[QuestionAnswerMapping] = []
    for item in data:
        mapping = QuestionAnswerMapping(
            db_id=item.get("db_id", ""),
            spider_question=item.get("SpiderQuestion", ""),
            spider_syn_question=item.get("SpiderSynQuestion", ""),
            query=item.get("query", ""),
            spider_syn_embedding=None  # Initial value set to None
        )
        qa_mappings.append(mapping)

    return qa_mappings


def custom_encoder(obj):
    """
    Custom JSON encoder function for objects that are not JSON serializable by default.

    Args:
        obj: The object to encode.

    Returns:
        The object's __dict__ if available.

    Raises:
        TypeError: If the object cannot be serialized.
    """
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def load_mapping_dbs(file_path_tables: str) -> Dict[str, MappingDB]:
    """
    Load the tables.json file and create MappingDB objects.

    The JSON file is expected to be a list where each element
    describes the schema of a database with the following keys:
      - 'db_id'
      - 'table_names'
      - 'table_names_original'
      - 'column_names'
      - 'column_names_original'

    Args:
        file_path_tables (str): Path to the tables.json file.

    Returns:
        Dict[str, MappingDB]: A dictionary with db_id as keys and MappingDB
        objects as values.
    """
    with open(file_path_tables, "r", encoding="utf-8") as file:
        tables_data = json.load(file)

    mapping_dbs: Dict[str, MappingDB] = {}

    for db_schema in tables_data:
        # 1) Extract database-specific information
        db_id = db_schema["db_id"]
        table_names = db_schema["table_names"]
        table_names_original = db_schema["table_names_original"]
        column_names = db_schema["column_names"]
        column_names_original = db_schema["column_names_original"]

        # 2) Create TableMapping objects
        table_mappings: List[TableMapping] = []
        for tname, tname_orig in zip(table_names, table_names_original):
            table_mappings.append(
                TableMapping(
                    table_name=tname,
                    original_table_name=tname_orig
                )
            )

        # 3) Create ColumnMapping objects
        column_mappings: List[ColumnMapping] = []
        for (tbl_idx, col_name), (_, col_name_orig) in zip(
            column_names, column_names_original
        ):
            if tbl_idx == -1:
                # -1 indicates "asterisk" or no specific table.
                table_name = ""
            else:
                # Use the table index to get the corresponding table name
                try:
                    table_name = table_names[tbl_idx]
                except IndexError:
                    table_name = ""
            column_mappings.append(
                ColumnMapping(
                    table_name=table_name,
                    column_name=col_name,
                    original_column_name=col_name_orig
                )
            )

        # 4) Create a MappingDB object for the database schema
        mapping_dbs[db_id] = MappingDB(
            db_id=db_id,
            table_mappings=table_mappings,
            column_mappings=column_mappings
        )

    print(f"Erstellte MappingDB-Objekte: {len(mapping_dbs)}")
    return mapping_dbs