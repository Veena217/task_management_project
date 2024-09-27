import mysql.connector
from mysql.connector import Error

class MySQLManager:
    @staticmethod
    def get_connection(host, user, password, database, port):
        """
        Establishes and returns a MySQL database connection.
        :param host: The MySQL server address
        :param user: The MySQL user name
        :param password: The MySQL user password
        :param database: The MySQL database name
        :param port: The MySQL port
        :return: MySQL connection object or None
        """
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            if connection.is_connected():
                print("Successfully connected to the database")
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    @staticmethod
    def execute_query(query, values, host, user, password, database, port):
        """
        Executes an SQL query with given values.
        :param query: The SQL query to execute
        :param values: The values to use with the query (tuple)
        :param host: The MySQL server address
        :param user: The MySQL user name
        :param password: The MySQL user password
        :param database: The MySQL database name
        :param port: The MySQL port
        """
        connection = MySQLManager.get_connection(host, user, password, database, port)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, values)
                connection.commit()
                print("Query executed successfully")
            except Error as e:
                print(f"Error while executing query: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")
        else:
            print("Failed to connect to the database")

    @staticmethod
    def fetch_all(query, host, user, password, database, port):
        """
        Executes a SELECT query and returns all results.
        :param query: The SQL query to execute
        :param host: The MySQL server address
        :param user: The MySQL user name
        :param password: The MySQL user password
        :param database: The MySQL database name
        :param port: The MySQL port
        :return: List of tuples representing query results
        """
        connection = MySQLManager.get_connection(host, user, password, database, port)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                print(f"Fetched {len(result)} rows")
                return result
            except Error as e:
                print(f"Error while fetching data: {e}")
                return []
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")
        else:
            print("Failed to connect to the database")
            return []
