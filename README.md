**# DataStats Package Documentation**

## Overview
DataStats is a Python package for statistical analysis of manufacturing data, featuring automated database management
and statistical calculations. The package handles SKU-based data analysis, stores results in MySQL, and supports both
manual and automated execution modes.

## Modules

# DatabaseManager

### _## Overview_

The DatabaseManager class provides a comprehensive interface for managing MySQL database operations, including 
connection management, database initialization, table operations, and data manipulation. This class is designed
to handle manufacturing quality control data with specific focus on specification limits and statistical measurements.

## Class Initialization
```python
DatabaseManager(host, username, password, database_name)
```

### Parameters
- `host`: The hostname where the MySQL server is running
- `username`: MySQL user credentials
- `password`: MySQL password for the specified user
- `database_name`: Name of the database to manage

## Core Methods

### Connection Management

#### connect_db()
Establishes a connection to the MySQL server.
- Returns: MySQL connection object or None if connection fails
- Logs errors if connection fails

#### close_connection()
Safely closes the database connection.
- Logs when connection is closed
- Should be called when database operations are complete

### Database Operations

#### init_db()
Creates a new database if it doesn't exist.
- Creates database using the name specified during initialization
- Returns: Success message or error message
- Implements automatic rollback on failure

#### check_db()
Verifies the current database connection.
- Returns: Current database name or None
- Logs errors if check fails

#### switch_db(db_name)
Switches to a specified database.
- Parameters:
  - `db_name`: Name of the database to switch to
- Logs success/failure messages
- Verifies current database before switching

### Table Operations

#### create_table(db_name, table_name)
Creates a table with a predefined schema for quality control data.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Name of the table to create
- Schema includes:
  - `id`: Auto-incrementing primary key
  - `sku`: Unique product identifier (VARCHAR(50))
  - `lsl`: Lower specification limit (DECIMAL)
  - `usl`: Upper specification limit (DECIMAL)
  - `mean`: Statistical mean (DECIMAL)
  - `variance`: Statistical variance (DECIMAL)
  - `std_dev`: Standard deviation (DECIMAL)
  - `sigma_level`: Six Sigma level (DECIMAL)
- Implements automatic rollback on failure

#### drop_table(db_name, table_name)
Removes a specified table from the database.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Name of the table to drop
- Logs success/failure messages

#### view_table(db_name, table_name)
Retrieves all records from a specified table.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Name of the table to view
- Returns: All records in the table
- Logs errors if query fails

### Data Management

#### update_table_default(db_name, table_name)
Populates the table with default quality control specifications.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Target table name
- Inserts default specifications for various products
- Uses IGNORE to prevent duplicate SKU entries
- Implements automatic rollback on failure

#### update_table(db_name, table_name, query, sku, param)
Executes custom update queries on the table.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Target table name
  - `query`: Custom SQL query to execute
  - `sku`: Product SKU
  - `param`: Parameter value to update
- Implements automatic rollback on failure
- Logs success/failure messages

#### get_lsl(db_name, table_name)
Retrieves lower specification limits for all products.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Source table name
- Returns: Dictionary mapping SKUs to their LSL values
- Return type: dict[str, float]

#### get_usl(db_name, table_name)
Retrieves upper specification limits for all products.
- Parameters:
  - `db_name`: Database name
  - `table_name`: Source table name
- Returns: Dictionary mapping SKUs to their USL values
- Return type: dict[str, float]

## Error Handling
- All methods implement try-except blocks for error handling
- Database operations use transaction management with automatic rollback
- Errors are logged using a logger instance
- Connection status is verified before operations

## Best Practices
1. Always close the connection using `close_connection()` when done
2. Verify connection status before operations
3. Use try-except blocks when calling methods
4. Check returned values for error conditions
5. Monitor logs for operation status and errors

## Example Usage
```python
# Initialize database manager
db_manager = DatabaseManager(
    host="localhost",
    username="user",
    password="password",
    database_name="quality_control"
)

# Initialize database and create table
db_manager.init_db()
db_manager.create_table("quality_control", "specifications")

# Insert default data
db_manager.update_table_default("quality_control", "specifications")

# Get specification limits
lsl_dict = db_manager.get_lsl("quality_control", "specifications")
usl_dict = db_manager.get_usl("quality_control", "specifications")

# Close connection when done
db_manager.close_connection()
```

## Dependencies
- mysql.connector
- logging (for logger instance)

## Note
This class is specifically designed for managing quality control specifications 
and statistical data. The schema is optimized for storing product specifications
and six sigma metrics.

## update_dbstats

### Overview
This module provides functionality for updating statistical measurements in a database table.
It includes functions for updating mean, standard deviation, variance, and sigma level calculations
for SKUs (Stock Keeping Units).


## Functions

### `update_mean(mean_json: dict, table: str) -> None`
Updates the mean values for SKUs in the specified database table.

#### Parameters:
- `mean_json` (dict): Dictionary containing SKU-mean pairs where:
  - key: SKU identifier (str)
  - value: calculated mean value (float)
- `table` (str): Name of the target database table

#### Usage Example:
```python
mean_data = {
    'SKU123': 45.67,
    'SKU456': 89.12
}
update_mean(mean_data, 'statistics_table')
```

### `update_std_dev(std_dev_json: dict, table: str) -> None`
Updates the standard deviation values for SKUs in the specified database table.

#### Parameters:
- `std_dev_json` (dict): Dictionary containing SKU-standard deviation pairs where:
  - key: SKU identifier (str)
  - value: calculated standard deviation value (float)
- `table` (str): Name of the target database table

#### Usage Example:
```python
std_dev_data = {
    'SKU123': 5.67,
    'SKU456': 3.21
}
update_std_dev(std_dev_data, 'statistics_table')
```

### `update_variance(variance_json: dict, table: str) -> None`
Updates the variance values for SKUs in the specified database table.

#### Parameters:
- `variance_json` (dict): Dictionary containing SKU-variance pairs where:
  - key: SKU identifier (str)
  - value: calculated variance value (float)
- `table` (str): Name of the target database table

#### Usage Example:
```python
variance_data = {
    'SKU123': 32.15,
    'SKU456': 10.30
}
update_variance(variance_data, 'statistics_table')
```

### `update_sigma(sigma_json: dict, table: str) -> None`
Updates the sigma level values for SKUs in the specified database table.

#### Parameters:
- `sigma_json` (dict): Dictionary containing SKU-sigma pairs where:
  - key: SKU identifier (str)
  - value: calculated sigma level value (float)
- `table` (str): Name of the target database table

#### Usage Example:
```python
sigma_data = {
    'SKU123': 3.0,
    'SKU456': 6.0
}
update_sigma(sigma_data, 'statistics_table')
```

## Database Schema
The module expects a database table with the following columns:
- `sku` (Primary Key)
- `mean`
- `std_dev`
- `variance`
- `sigma_level`

## Dependencies
- DataStats.app.core.config
- DataStats.app.database.db_manager

## Error Handling
All database operations are handled by the `db_manager` module. Refer to its section above for specific
error handling details.

## Notes
- All update functions use MySQL's `ON DUPLICATE KEY UPDATE` functionality to either insert new records
- or update existing ones
- The module uses configuration values from `config.py` for database and table names
- Each statistical measure (mean, std_dev, variance, sigma) is updated independently


### statistics.stats
Statistical calculation module providing core analytical functions.

Functions:
```python
def get_mean(df: pd.DataFrame) -> dict
def get_variance(df: pd.DataFrame) -> dict
def get_std_dev(df: pd.DataFrame) -> dict
def get_sigma(df: pd.DataFrame, LSL: dict, USL: dict) -> dict
```

The sigma calculation uses: σ = min((USL - μ)/σ, (μ - LSL)/σ)

### automation.auto
Handles automated execution scheduling.

Features:
- Weekly execution (Mondays at 8:00 AM)
- Configurable via AUTO_RUN setting
- Sleep interval: 60 seconds between schedule checks

### manual_run
Executes the complete analysis pipeline:
1. Reads Excel data
2. Creates/updates database table
3. Retrieves specification limits
4. Calculates statistics
5. Updates database with results

### main
Entry point supporting three execution modes:
- default: Runs immediate analysis
- auto: Enables scheduled execution
- manual: User-triggered execution

Usage:
```bash
python main.py [default|auto|manual]
```

# Database Initialization

## Overview
Initializes the main database manager instance using configuration parameters.

## Implementation
```python
db_manager = DatabaseManager(
    host=DB_HOST,
    username=DB_USER,
    password=DB_PASSWORD,
    database_name=DB_NAME
)
```

## Configuration Requirements
- DB_HOST: Database server hostname
- DB_USER: Database username
- DB_PASSWORD: Database password
- DB_NAME: Target database name
- TABLE_NAME: Default table name for operations

## Usage
Import the configured database manager:

```python
from DataStats.DataStats.app import db_manager
```

## Database Schema
```sql
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    lsl DECIMAL(10, 2) DEFAULT NULL,
    usl DECIMAL(10, 2) DEFAULT NULL,
    mean DECIMAL(10, 2) DEFAULT NULL,
    variance DECIMAL(10, 2) DEFAULT NULL,
    std_dev DECIMAL(10, 2) DEFAULT NULL,
    sigma_level DECIMAL(10, 2) DEFAULT NULL
);
```

## Global Dependencies
- pandas
- mysql-connector-python
- schedule
- openpyxl
- python-dotenv

## Configuration
Required environment variables:
- TABLE_NAME
- EXCEL_FILE
- AUTO_RUN
- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME
- TABLE_NAME

## Error Handling
- Database operations use try-except blocks with rollback
- Zero standard deviation cases are handled in sigma calculations
- Connection status is verified before operations

## Installation
To use this module, ensure you have the following dependencies: