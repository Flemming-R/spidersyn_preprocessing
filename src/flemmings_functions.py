import json
from typing import List

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
