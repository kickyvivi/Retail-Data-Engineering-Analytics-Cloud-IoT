import jaydebeapi
import os

# Path to the Simba JDBC driver JAR files
driver_path = "C:/apache-hop-client-2.11.0/hop/lib/jdbc/GoogleBigQueryJDBC42.jar"
additional_jars = [
    	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/animal-sniffer-annotations-1.24.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/annotations-4.1.1.4.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/api-common-2.38.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/auto-value-1.11.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/auto-value-annotations-1.11.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/avro-1.11.4.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/clickhouse-jdbc-0.7.1-patch1-all.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/client-1.0.0-beta.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/common-1.0.0-beta.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/commons-codec-1.17.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/commons-compress-1.27.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/conscrypt-openjdk-uber-2.5.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/crate-jdbc-2.7.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/derbyclient-10.17.1.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/duckdb_jdbc-1.0.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/error_prone_annotations-2.33.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/EULA.txt",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/failureaccess-1.0.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/gax-2.55.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/gax-grpc-2.55.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-api-client-2.7.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-api-services-bigquery-v2-rev20240919-2.0.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-auth-library-credentials-1.28.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-auth-library-oauth2-http-1.28.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-cloud-bigquerystorage-3.9.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-cloud-core-2.45.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-http-client-1.45.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-http-client-apache-v2-1.45.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-http-client-gson-1.45.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/google-oauth-client-1.36.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/GoogleBigQueryJDBC42.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-auth-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-context-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-google-cloud-bigquerystorage-v1-3.9.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-google-cloud-bigquerystorage-v1beta1-0.181.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-google-cloud-bigquerystorage-v1beta2-0.181.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-googleapis-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-grpclb-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-inprocess-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-protobuf-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-protobuf-lite-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-stub-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/grpc-util-1.67.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/gson-2.11.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/guava-33.3.1-jre.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/h2-2.2.224.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/hop-databases-cratedb-2.11.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/hsqldb-2.7.4.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/httpclient-4.5.14.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/httpcore-4.4.16.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/j2objc-annotations-3.0.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jackson-annotations-2.14.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jackson-core-2.17.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jackson-databind-2.14.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/javax.annotation-api-1.3.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jna-4.2.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jna-platform-4.2.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/joda-time-2.13.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/json-20240303.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/jsr305-3.0.2.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/listenablefuture-9999.0-empty-to-avoid-conflict-with-guava.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/monetdb-jdbc-3.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/mssql-jdbc-12.6.3.jre11.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/opencensus-api-0.31.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/opencensus-contrib-http-util-0.31.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/opentelemetry-api-1.42.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/opentelemetry-context-1.42.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/org.osgi.core-4.3.1.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/org.osgi.enterprise-4.2.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/perfmark-api-0.27.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/postgresql-42.7.4.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-cloud-bigquerystorage-v1-3.9.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-cloud-bigquerystorage-v1alpha-3.9.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-cloud-bigquerystorage-v1beta1-0.181.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-cloud-bigquerystorage-v1beta2-0.181.3.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-common-protos-2.46.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/proto-google-iam-v1-1.41.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/protobuf-java-3.25.5.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/protobuf-java-util-3.25.5.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/redshift-jdbc42-2.1.0.30.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/slf4j-api-1.7.36.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/snowflake-jdbc-3.20.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/sqlite-jdbc-3.46.0.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/threetenbp-1.7.0.jar",
	"C:/apache-hop-client-2.11.0/hop/lib/jdbc/waffle-jna-1.7.5.jar"
    # Add other JARs from the lib directory if necessary
]

# Combine all JAR files into the classpath
classpath = os.pathsep.join([driver_path] + additional_jars)

# Database connection URL
jdbc_url = (
    "jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;"
    "ProjectId=retail-iot-project;"
    "OAuthType=0;"
    "OAuthServiceAcctEmail=data-generator@retail-iot-project.iam.gserviceaccount.com;"
    "OAuthPvtKeyPath=C:/apache-hop-client-2.11.0/hop/config/bigquery_service_account.json;"
    "DatasetId=staging;"
)

# JDBC driver class for Simba BigQuery
jdbc_driver_class = "com.simba.googlebigquery.jdbc42.Driver"

# Empty credentials (BigQuery uses service account key instead)
jdbc_username = ""
jdbc_password = ""

try:
    # Establish the connection
    conn = jaydebeapi.connect(
        jdbc_driver_class,
        jdbc_url,
        [],
        classpath,
    )
    print("Connection successful!")

    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables")
    for table in cursor.fetchall():
        print(table)
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error occurred: {e}")
