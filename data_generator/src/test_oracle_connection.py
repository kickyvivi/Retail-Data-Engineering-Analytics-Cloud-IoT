from io_utils import get_oracle_connection

CONFIG_PATH = "config/oracle_config.json"

if __name__ == "__main__":
    try:
        connection = get_oracle_connection(CONFIG_PATH)
        print("Connection successful:", connection.version)
        connection.close()
    except oracledb.DatabaseError as e:
        print(f"Database connection failed: {e}")
