from sqlalchemy import create_engine

# RDB connection info
user_name = "username"
password = "password"
host = "localhost"
port = "5432"
database_name = "database_name"

# refactor this methdo to pass like username, password to get the connection string
def get_db_connection():
    engine = create_engine(f"postgresql://{user_name}:{password}@{host}:{port}/{database_name}")
    return engine

# Example usage
# input_directory = "path/to/csv_files"
# db_connection_string = "postgresql://username:password@localhost:5432/database_name"
# export_csv_to_rdb(input_directory, db_connection_string)