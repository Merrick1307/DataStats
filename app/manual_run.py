from DataStats.app.core import logger

import pandas as pd

from DataStats.app.DataVisuals import visualize
from DataStats.app.core.config import (
    TABLE_NAME, EXCEL_FILE, DB_NAME, VISUALIZE
)
from DataStats.app.database import db_manager
from DataStats.app.database.update_dbstats import (
    update_mean, update_std_dev, update_variance,
    update_sigma
)
from DataStats.app.statistics import stats


def do_analysis():
    """
     Performs statistical analysis on manufacturing data
     from Excel file and updates database.

     Process:
     1. Reads data from configured Excel file
     2. Creates/updates database table with default values
     3. Retrieves LSL/USL specification limits
     4. Calculates statistical metrics (mean, std dev, variance, sigma)
     5. Updates database with calculated values

     Configuration Required:
         - TABLE_NAME: Target database table
         - EXCEL_FILE: Source Excel file path

     Returns:
         str: Completion message directing to info.log for details

     Note:
         Expects Excel file with columns 'Sku' and 'Value'
         Database table must have schema matching
         DatabaseManager.create_table()
     """
    file_name = EXCEL_FILE
    data = pd.read_excel(file_name)
    df = pd.DataFrame(data)

    db_manager.create_table(DB_NAME, TABLE_NAME)
    db_manager.update_table_default(DB_NAME, TABLE_NAME)

    LSL = db_manager.get_lsl(DB_NAME, table_name="noodles_data")
    USL = db_manager.get_usl(DB_NAME, table_name="noodles_data")
    mean_dict = stats.get_mean(df)
    std_dev_dict = stats.get_std_dev(df)
    variance_dict = stats.get_variance(df)
    sigma_dict = stats.get_sigma(df, LSL, USL)
    update_mean(mean_dict, TABLE_NAME)
    update_variance(variance_dict, TABLE_NAME)
    update_std_dev(std_dev_dict, TABLE_NAME)
    update_sigma(sigma_dict, TABLE_NAME)

    if VISUALIZE:
        visualize()

    return logger.info(
        "Analysis complete!, check the .log file for details, "
        "and current working directory for the visualizations"
    )
