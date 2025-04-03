from typing import List, Dict, Optional
import numpy as np
import sqlite3

class QuestionAnswerMapping:
    """
    Speichert die Zuordnung zwischen:
      - db_id: Identifikation der Datenbank
      - spider_question: Die originale Frage aus dem Spider-Datenset
      - spider_syn_question: Die synthetisierte Version der Frage (SpiderSyn)
      - query: Das zugehörige SQL-Query (aus dem Datenset)
      - generated_query: Ein von der Text-to-SQL Komponente generierter Query
      - spider_syn_embedding: Ein Embedding-Vektor für die SpiderSyn-Frage
    """
    def __init__(self, 
                 db_id: str, 
                 spider_question: str, 
                 spider_syn_question: str, 
                 query: str, 
                 generated_query: Optional[str] = None,
                 spider_syn_embedding: Optional[np.ndarray] = None):
        self.db_id = db_id
        self.spider_question = spider_question
        self.spider_syn_question = spider_syn_question
        self.query = query
        self.generated_query = generated_query
        self.spider_syn_embedding = spider_syn_embedding

class TableMapping:
    """
    Speichert die Zuordnung zwischen dem verarbeiteten Tabellennamen und dem Originalnamen.
    """
    def __init__(self, table_name: str, original_table_name: str):
        self.table_name = table_name
        self.original_table_name = original_table_name

class ColumnMapping:
    """
    Speichert die Zuordnung zwischen dem verarbeiteten Spaltennamen und dem Originalnamen.
    Zusätzlich wird festgehalten, zu welcher Tabelle die Spalte gehört.
    """
    def __init__(self, table_name: str, column_name: str, original_column_name: str):
        self.table_name = table_name
        self.column_name = column_name
        self.original_column_name = original_column_name

class MappingDB:
    """
    Speichert für eine bestimmte Datenbank (über db_id) die
    Mapping-Informationen der Tabellen und Spalten, sowie zugehörige Embeddings.
    """
    def __init__(self, 
                 db_id: str, 
                 table_mappings: List[TableMapping], 
                 column_mappings: List[ColumnMapping]):
        self.db_id = db_id
        self.table_mappings = table_mappings
        self.column_mappings = column_mappings
        # Hier werden Embeddings als Dictionary abgelegt:
        # key: table_name bzw. column_name, value: np.ndarray (Embedding-Vektor)
        self.table_embeddings: Dict[str, np.ndarray] = {}
        self.column_embeddings: Dict[str, np.ndarray] = {}

    def add_table_embedding(self, table_name: str, embedding: np.ndarray):
        self.table_embeddings[table_name] = embedding

    def add_column_embedding(self, column_name: str, embedding: np.ndarray):
        self.column_embeddings[column_name] = embedding

class SpiderDatabase:
    """
    Schnittstelle zu einer gefüllten SQLite-Datenbank,
    die die tatsächlichen Daten aus dem Spider-Datenset enthält.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
    
    def query(self, sql_query: str):
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()

    def close(self):
        self.connection.close()
