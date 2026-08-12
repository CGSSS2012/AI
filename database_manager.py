"""
Database Manager Module
Handles all database operations (MySQL, PostgreSQL, SQLite)
"""

from sqlalchemy import create_engine, inspect, text, String, Integer, Float, Boolean, DateTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        self.connections = {}  # Store multiple database connections
        self.metadata = {}     # Store metadata for each database

    def connect_database(self, db_type, host=None, port=None, username=None, password=None, database=None, file_path=None):
        """
        Connect to a database
        db_type: 'mysql', 'postgresql', 'sqlite'
        """
        try:
            if db_type.lower() == 'sqlite':
                connection_string = f"sqlite:///{file_path}"
            elif db_type.lower() == 'mysql':
                connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            elif db_type.lower() == 'postgresql':
                connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            else:
                raise ValueError(f"Unsupported database type: {db_type}")

            engine = create_engine(connection_string)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            db_id = f"{db_type}_{database or file_path}_{len(self.connections)}"
            self.connections[db_id] = {
                'engine': engine,
                'type': db_type,
                'config': {
                    'host': host,
                    'port': port,
                    'username': username,
                    'database': database,
                    'file_path': file_path
                }
            }
            
            return f"Connected to {db_type} database successfully. ID: {db_id}"
        
        except Exception as e:
            raise Exception(f"Database connection failed: {str(e)}")

    def get_all_databases(self):
        """Get list of all connected databases"""
        return [
            {
                'id': db_id,
                'type': info['type'],
                'database': info['config'].get('database', info['config'].get('file_path'))
            }
            for db_id, info in self.connections.items()
        ]

    def get_tables(self, db_id):
        """Get all table names in a database"""
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        inspector = inspect(engine)
        return inspector.get_table_names()

    def create_table(self, db_id, table_config):
        """
        Create a new table
        table_config: {
            'name': 'table_name',
            'columns': [
                {'name': 'id', 'type': 'INTEGER', 'primary_key': True, 'autoincrement': True},
                {'name': 'username', 'type': 'VARCHAR(255)', 'nullable': False},
                {'name': 'email', 'type': 'VARCHAR(255)', 'nullable': False, 'unique': True}
            ]
        }
        """
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        table_name = table_config['name']
        columns = table_config['columns']

        # Build SQL CREATE TABLE statement
        sql_parts = [f"CREATE TABLE IF NOT EXISTS {table_name} ("]
        col_defs = []

        for col in columns:
            col_def = f"{col['name']} {col['type']}"
            
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('autoincrement'):
                col_def += " AUTO_INCREMENT"
            if col.get('nullable') is False:
                col_def += " NOT NULL"
            if col.get('unique'):
                col_def += " UNIQUE"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            
            col_defs.append(col_def)

        sql_parts.append(", ".join(col_defs))
        sql_parts.append(")")
        
        sql = " ".join(sql_parts)

        try:
            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
            return f"Table '{table_name}' created successfully"
        except Exception as e:
            raise Exception(f"Failed to create table: {str(e)}")

    def get_table_schema(self, db_id, table_name):
        """Get the schema of a table"""
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        inspector = inspect(engine)
        
        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        
        return {
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }

    def delete_table(self, db_id, table_name):
        """Delete a table"""
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        
        try:
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                conn.commit()
            return f"Table '{table_name}' deleted successfully"
        except Exception as e:
            raise Exception(f"Failed to delete table: {str(e)}")

    def add_column(self, db_id, table_name, column_config):
        """
        Add a column to an existing table
        column_config: {'name': 'column_name', 'type': 'VARCHAR(255)', 'nullable': True}
        """
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        col_name = column_config['name']
        col_type = column_config['type']
        nullable = "NULL" if column_config.get('nullable', True) else "NOT NULL"
        
        sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {nullable}"
        
        try:
            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
            return f"Column '{col_name}' added to table '{table_name}'"
        except Exception as e:
            raise Exception(f"Failed to add column: {str(e)}")

    def get_table_data(self, db_id, table_name, limit=100):
        """Get data from a table"""
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}"))
                rows = result.fetchall()
                columns = result.keys()
                
                data = [dict(zip(columns, row)) for row in rows]
                return data
        except Exception as e:
            raise Exception(f"Failed to retrieve data: {str(e)}")

    def insert_data(self, db_id, table_name, data):
        """
        Insert data into a table
        data: {'column1': 'value1', 'column2': 'value2'}
        """
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
        
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        
        try:
            with engine.connect() as conn:
                conn.execute(text(sql))
                conn.commit()
            return f"Data inserted into '{table_name}' successfully"
        except Exception as e:
            raise Exception(f"Failed to insert data: {str(e)}")

    def execute_query(self, db_id, query):
        """Execute a custom SQL query"""
        if db_id not in self.connections:
            raise Exception(f"Database {db_id} not found")
        
        engine = self.connections[db_id]['engine']
        
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query))
                if result.description:
                    rows = result.fetchall()
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in rows]
                return {"message": "Query executed successfully"}
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
