import pandas as pd
from sqlalchemy import create_engine

def export_csv_to_rdb(input_dir, db_connection_string):
    # Get database connection
    engine = get_db_connection(db_connection_string)

    # Read CSV files
    hard_drive_by_date_df = pd.read_csv(f"{input_dir}/hard_drive_by_date.csv")
    hard_drive_by_year_df = pd.read_csv(f"{input_dir}/hard_drive_by_year.csv")

    # Export DataFrames to RDB
    export_df_to_rdb(hard_drive_by_date_df, 'hard_drive_by_date', engine)
    export_df_to_rdb(hard_drive_by_year_df, 'hard_drive_by_year', engine)

def export_df_to_rdb(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# refactor this methdo to pass like username, password to get the connection string
def get_db_connection(username, password, host, port, database_name):
    engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database_name}")
    return engine

# Example usage
# input_directory = "path/to/csv_files"
# db_connection_string = "postgresql://username:password@localhost:5432/database_name"
# export_csv_to_rdb(input_directory, db_connection_string)