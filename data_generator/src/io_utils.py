import oracledb
import json

def get_oracle_connection(config_path):
    """
    Establish a connection to the Oracle ADB using TLS.

    Args:
        config_path (str): Path to the JSON configuration file.
    Returns:
        oracledb.Connection: Oracle database connection object.
    """
    # Load config
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Build the DSN
    dsn = f"(description=(retry_count=20)(retry_delay=3)" \
          f"(address=(protocol=tcps)(port={config['dsn']['port']})(host={config['dsn']['host']}))" \
          f"(connect_data=(service_name={config['dsn']['service_name']}))" \
          f"(security=(ssl_server_dn_match=yes)))"

    # Connect to the database
    connection = oracledb.connect(
        user=config["user"],
        password=config["password"],
        dsn=dsn
    )
    return connection
