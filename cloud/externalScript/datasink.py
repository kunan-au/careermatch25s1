import pymysql
import sys

# Database A (source, local)
db_a_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "admin",
    "password": "",  # Replace with your password
    "database": "imba"
}

# Database B (target, RDS)
db_b_config = {
    "host": "",
    "port": 3306,
    "user": "admin",
    "password": "",  # Replace with your password
    "database": ""
}


def copy_tables():
    try:
        # Connect to both databases
        print("Connecting to Database A (local)...")
        conn_a = pymysql.connect(**db_a_config)
        print("✅ Successfully connected to Database A.")
        
        print("Connecting to Database B (RDS)...")
        conn_b = pymysql.connect(host=db_b_config["host"],
                                 port=db_b_config["port"],
                                 user=db_b_config["user"],
                                 password=db_b_config["password"])
        print("✅ Successfully connected to Database B.\n")

        cursor_a = conn_a.cursor()
        cursor_b = conn_b.cursor()

        # Ensure Database B exists
        print("Checking if Database B exists...")
        cursor_b.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor_b.fetchall()]
        if db_b_config["database"] not in databases:
            print(f"Database '{db_b_config['database']}' does not exist. Creating...")
            cursor_b.execute(f"CREATE DATABASE {db_b_config['database']};")
            print(f"✅ Database '{db_b_config['database']}' created successfully.")
        cursor_b.execute(f"USE {db_b_config['database']};")

        # Disable foreign key checks temporarily
        print("Disabling foreign key checks...")
        cursor_b.execute("SET FOREIGN_KEY_CHECKS=0;")
        print("✅ Foreign key checks disabled.\n")

        # Fetch all tables from Database A
        print("Fetching all tables from Database A...")
        cursor_a.execute("SHOW TABLES;")
        tables = cursor_a.fetchall()
        total_tables = len(tables)
        print(f"Found {total_tables} tables to migrate.\n")

        # Loop through all tables
        for t_index, (table_name,) in enumerate(tables, start=1):
            print(f"🚀 Processing table {t_index}/{total_tables}: {table_name}")

            try:
                # Get CREATE TABLE statement from Database A
                cursor_a.execute(f"SHOW CREATE TABLE {table_name};")
                create_table_sql = cursor_a.fetchone()[1]

                # Drop and recreate table in Database B
                cursor_b.execute(f"DROP TABLE IF EXISTS {table_name};")
                cursor_b.execute(create_table_sql)
                print(f"✅ Table {table_name} created in Database B.\n")

                # Copy data row-by-row with progress printing
                print(f"Fetching rows from table '{table_name}' in Database A...")
                cursor_a.execute(f"SELECT * FROM {table_name};")
                rows = cursor_a.fetchall()
                total_rows = len(rows)
                print(f"✅ Found {total_rows} rows in table '{table_name}'. Starting data transfer...\n")

                if total_rows > 0:
                    # Generate INSERT statement
                    columns_query = f"DESCRIBE {table_name};"
                    cursor_a.execute(columns_query)
                    columns = [col[0] for col in cursor_a.fetchall()]
                    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))});"

                    # Insert rows with real-time row-by-row progress
                    for i, row in enumerate(rows, start=1):
                        try:
                            cursor_b.execute(insert_query, row)
                            conn_b.commit()
                            # Print progress row-by-row in real-time
                            print(f"Copying row {i}/{total_rows} from '{table_name}'", end="\r", flush=True)
                        except Exception as e:
                            print(f"\n❌ Error copying row {i} from '{table_name}': {e}")
                            break

                print(f"\n✅ Table {table_name} migrated successfully.\n")

            except Exception as e:
                print(f"\n❌ An error occurred while processing table {table_name}: {e}. Skipping.\n")
                continue

        # Re-enable foreign key checks
        cursor_b.execute("SET FOREIGN_KEY_CHECKS=1;")
        print("\n✅ Foreign key checks re-enabled.")
        print("✅ All tables have been processed successfully.")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # Close database connections
        if 'conn_a' in locals() and conn_a:
            conn_a.close()
        if 'conn_b' in locals() and conn_b:
            conn_b.close()
        print("\nMigration completed.")


if __name__ == "__main__":
    copy_tables()
