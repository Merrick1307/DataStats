import mysql.connector
from mysql.connector import Error
from DataStats.app.core import logger


class DatabaseManager:
    """
    A class to manage MySQL database operations for
    quality control data.

    This class handles database connections, initialization,
    and various operations including table management and
    data manipulation for quality control metrics.

    Attributes:
        server (dict): Database connection parameters including
                       host, user, and password
        database_name (str): Name of the database to manage
        connection: MySQL connection object

    Example:
        >>> db = DatabaseManager("localhost", "user", "password", "dufil_db")
        >>> db.connect_db()
        >>> db.init_db()
        >>> db.close_connection()
    """

    def __init__(self, host, username, password, database_name):
        """
        Initialize DatabaseManager with connection parameters.

        Args:
            host (str): MySQL server hostname
            username (str): MySQL username
            password (str): MySQL password
            database_name (str): Name of the database to manage
        """
        self.server = {
            'host': host,
            'user': username,
            'password': password
        }
        self.database_name = database_name
        self.connection = None

    def connect_db(self):
        """
        Establish connection to MySQL server.

        Returns:
            MySQLConnection: Connection object if successful, None otherwise

        Raises:
            mysql.connector.Error: If connection fails
        """
        try:
            self.connection = mysql.connector.connect(**self.server)
            return self.connection
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return None

    def init_db(self):
        """
        Initialize database if it doesn't exist.

        Creates a new database using the name specified during initialization.
        Automatically handles connection and transaction management.

        Returns:
            str: Success or error message

        Raises:
            mysql.connector.Error: If database creation fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
                )
                self.connection.commit()
                return logger.info(
                    f"Database '{self.database_name}' created successfully"
                )
        except Error as e:
            if self.connection:
                self.connection.rollback()
            return f"Error creating database: {e}"

    def check_db(self):
        """
        Check current database connection status.

        Returns:
            str: Name of current database if connected, None otherwise

        Raises:
            mysql.connector.Error: If database check fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE()")
                result = cursor.fetchone()
                return result[0] if result else None
        except Error as e:
            return logger.error(f"Error checking database: {e}")

    def switch_db(self, db_name):
        """
        Switch to a different database.

        Args:
            db_name (str): Name of the database to switch to

        Returns:
            str: Success or error message

        Raises:
            mysql.connector.Error: If database switch fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()
            check_current_db = self.check_db()
            if check_current_db != db_name:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"USE {db_name}")
                    return logger.info(
                        f"Switched to database '{db_name}'"
                    )
        except Error as e:
            return logger.error(f"Error switching database: {e}")

    def create_table(self, db_name, table_name):
        """
        Create a table for quality control specifications.

        Creates a table with columns for SKU, specification limits,
        and statistical measurements.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table to create

        Returns:
            str: Success or error message

        Schema:
            - id: INT AUTO_INCREMENT PRIMARY KEY
            - sku: VARCHAR(50) UNIQUE NOT NULL
            - lsl: DECIMAL(10, 2) DEFAULT NULL
            - usl: DECIMAL(10, 2) DEFAULT NULL
            - mean: DECIMAL(10, 2) DEFAULT NULL
            - variance: DECIMAL(10, 2) DEFAULT NULL
            - std_dev: DECIMAL(10, 2) DEFAULT NULL
            - sigma_level: DECIMAL(10, 2) DEFAULT NULL

        Raises:
            mysql.connector.Error: If table creation fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                create_table_query = f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sku VARCHAR(50) UNIQUE NOT NULL,
                        lsl DECIMAL(10, 2) DEFAULT NULL,
                        usl DECIMAL(10, 2) DEFAULT NULL,
                        mean DECIMAL(10, 2) DEFAULT NULL,
                        variance DECIMAL(10, 2) DEFAULT NULL,
                        std_dev DECIMAL(10, 2) DEFAULT NULL,
                        sigma_level DECIMAL(10, 2) DEFAULT NULL
                    );"""
                cursor.execute(create_table_query)
                self.connection.commit()
                return logger.info(
                    f"Table '{table_name}' created successfully"
                )
        except Error as e:
            logger.error(f"Error creating table: {e}")
            self.connection.rollback()

    def drop_table(self, db_name, table_name):
        """
        Drop a table from the database.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table to drop

        Returns:
            str: Success or error message

        Raises:
            mysql.connector.Error: If table deletion fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                cursor.execute(
                    f"""DROP TABLE IF EXISTS {table_name}
                    """
                )
            return logger.debug(
                f"table: {table_name}, deleted successfully!"
            )
        except Error as e:
            return logger.error(e)

    def view_table(self, db_name, table_name):
        """
        Retrieve all records from a table.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table to view

        Returns:
            list: List of tuples containing all records in the table

        Raises:
            mysql.connector.Error: If query fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                select_query = f"SELECT * FROM {table_name}"
                cursor.execute(select_query)
                results = cursor.fetchall()
                return results
        except Error as e:
            logger.error(e)

    def update_table_default(self, db_name, table_name):
        """
        Insert default quality control specifications into the table.

        Inserts predefined specification limits for various products.
        Uses INSERT IGNORE to prevent duplicate SKU entries.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table to update

        Returns:
            str: Success or error message

        Raises:
            mysql.connector.Error: If data insertion fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                insert_query = f"""
                    INSERT IGNORE INTO {table_name} (sku, lsl, usl)
                    VALUES 
                        ('Ochk 70g', 62.00, 68.00),
                        ('Mmchk 70g', 64.00, 68.00),
                        ('Rchk 120g', 112.00, 122.00),
                        ('RCHK 70g', 66.00, 72.00),
                        ('Mchk 70g', 64.00, 68.00),
                        ('Rchk 180g', 168.00, 182.00);
                """
                cursor.execute(insert_query)
                self.connection.commit()
                logger.info(
                    f"Data inserted into table '{table_name}' "
                    f"successfully"
                )
        except Error as e:
            logger.error(f"Error inserting data: {e}")
            self.connection.rollback()

    def update_table(self, db_name, table_name, query, sku, param):
        """
        Execute custom update query on the table.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table to update
            query (str): SQL query to execute
            sku (str): Product SKU to update
            param: Value to update

        Returns:
            str: Success or error message

        Raises:
            mysql.connector.Error: If update fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                cursor.execute(query, (sku, param))
                self.connection.commit()
                logger.info(
                    f"Data inserted into table '{table_name}' "
                    f"successfully"
                )
        except Error as e:
            logger.error(
                f"Error inserting data: {e}, All changes undone"
            )
            self.connection.rollback()

    def get_lsl(self, db_name, table_name) -> dict:
        """
        Get lower specification limits for all products.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table

        Returns:
            dict: Dictionary mapping SKUs to their LSL values {sku: lsl}

        Raises:
            mysql.connector.Error: If query fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT sku, lsl FROM {table_name}")
                results = cursor.fetchall()
                self.connection.commit()
            return {sku: float(lsl) for sku, lsl in results}
        except Error as e:
            logger.error(f"Error getting LSL: {e}")

    def get_usl(self, db_name, table_name) -> dict:
        """
        Get upper specification limits for all products.

        Args:
            db_name (str): Name of the database
            table_name (str): Name of the table

        Returns:
            dict: Dictionary mapping SKUs to their USL values {sku: usl}

        Raises:
            mysql.connector.Error: If query fails
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect_db()

            self.switch_db(db_name=db_name)
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT sku, usl FROM {table_name}")
                results = cursor.fetchall()
                self.connection.commit()
            return {sku: float(usl) for sku, usl in results}
        except Error as e:
            logger.error(f"Error getting USL: {e}")

    def close_connection(self):
        """
        Close the database connection.

        Safely closes the MySQL connection if it exists and is connected.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.debug("Database connection closed")
