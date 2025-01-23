from DataStats.app.core.config import TABLE_NAME, DB_NAME
from DataStats.app.database import db_manager


def update_mean(mean_json: dict, table: str) -> None:
    """
    Updates mean values for SKUs in the specified database table.

    This function takes a dictionary of SKU-mean pairs and updates or inserts
    the mean values in the database. If a SKU already exists, its mean value
    is updated; if it doesn't exist, a new record is created.

    Args:
        mean_json (dict): Dictionary containing SKU-mean pairs.
            key: SKU identifier (str)
            value: calculated mean value (float)
        table (str): Name of the target database table

    Returns:
        None

    Example:
        >>> mean_data = {'SKU123': 45.67, 'SKU456': 89.12}
        >>> update_mean(mean_data, 'statistics_table')

    Note:
        Uses MySQL's ON DUPLICATE KEY UPDATE functionality for upsert operations.
    """
    for sku, mean in mean_json.items():
        mean_query = f"""
                INSERT INTO {table} (sku, mean) 
                VALUES (%s, %s) ON DUPLICATE KEY 
                UPDATE mean=VALUES(mean) 
                """
        db_manager.update_table(
            DB_NAME, table, mean_query, sku, mean
        )


def update_std_dev(std_dev_json: dict, table: str) -> None:
    """
    Updates standard deviation values for SKUs in the specified database table.

    This function takes a dictionary of SKU-standard deviation pairs and updates
    or inserts the standard deviation values in the database. If a SKU already
    exists, its standard deviation value is updated; if it doesn't exist, a new
    record is created.

    Args:
        std_dev_json (dict): Dictionary containing SKU-standard deviation pairs.
            key: SKU identifier (str)
            value: calculated standard deviation value (float)
        table (str): Name of the target database table

    Returns:
        None

    Example:
        >>> std_dev_data = {'SKU123': 5.67, 'SKU456': 3.21}
        >>> update_std_dev(std_dev_data, 'statistics_table')

    Note:
        Uses MySQL's ON DUPLICATE KEY UPDATE functionality for upsert operations.
    """
    for sku, std_dev in std_dev_json.items():
        std_dev_query = f"""
                INSERT INTO {table} (sku, std_dev)  
                VALUES (%s, %s) ON DUPLICATE KEY 
                UPDATE std_dev=VALUES(std_dev) 
                """
        db_manager.update_table(
            DB_NAME, table, std_dev_query, sku, std_dev
        )


def update_variance(variance_json: dict, table: str) -> None:
    """
    Updates variance values for SKUs in the specified database table.

    This function takes a dictionary of SKU-variance pairs and updates or
    inserts the variance values in the database. If a SKU already exists,
    its variance value is updated; if it doesn't exist, a new record is created.

    Args:
        variance_json (dict): Dictionary containing SKU-variance pairs.
            key: SKU identifier (str)
            value: calculated variance value (float)
        table (str): Name of the target database table

    Returns:
        None

    Example:
        >>> variance_data = {'SKU123': 32.15, 'SKU456': 10.30}
        >>> update_variance(variance_data, 'statistics_table')

    Note:
        Uses MySQL's ON DUPLICATE KEY UPDATE functionality for upsert operations.
    """
    for sku, variance in variance_json.items():
        variance_query = f"""
                INSERT INTO {table} (sku, variance)  
                VALUES (%s, %s) ON DUPLICATE KEY 
                UPDATE variance=VALUES(variance) 
                """
        db_manager.update_table(
            DB_NAME, table, variance_query, sku, variance
        )


def update_sigma(sigma_json: dict, table: str) -> None:
    """
    Updates sigma level values for SKUs in the specified database table.

    This function takes a dictionary of SKU-sigma pairs and updates or inserts
    the sigma level values in the database. If a SKU already exists, its sigma
    level value is updated; if it doesn't exist, a new record is created.

    Args:
        sigma_json (dict): Dictionary containing SKU-sigma pairs.
            key: SKU identifier (str)
            value: calculated sigma level value (float)
        table (str): Name of the target database table

    Returns:
        None

    Example:
        >>> sigma_data = {'SKU123': 3.0, 'SKU456': 6.0}
        >>> update_sigma(sigma_data, 'statistics_table')

    Note:
        Uses MySQL's ON DUPLICATE KEY UPDATE functionality for upsert operations.
    """
    for sku, sigma in sigma_json.items():
        sigma_query = f"""
                INSERT INTO {table} (sku, sigma_level)  
                VALUES (%s, %s) ON DUPLICATE KEY 
                UPDATE sigma_level=VALUES(sigma_level) 
                """
        db_manager.update_table(
            DB_NAME, TABLE_NAME, sigma_query, sku, sigma
        )