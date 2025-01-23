from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from DataStats.app.core import DB_NAME
from DataStats.app.core.config import TABLE_NAME, AUTO_RUN
from DataStats.app.database import db_manager

def visualize():
    get_updated_db = db_manager.view_table(DB_NAME, TABLE_NAME)
    data = get_updated_db
    # Convert to DataFrame
    updated_df = pd.DataFrame(data, columns=[
        'Serial', 'SKU', 'LSL', 'USL', 'Mean',
        'Variance', 'Standard_Deviation', 'Sigma_Level'
    ])
    # Calculate control limits
    # Upper control limit
    updated_df['UCL'] = updated_df['Mean'] + 3 * updated_df['Standard_Deviation']
    # Lower control limit
    updated_df['LCL'] = updated_df['Mean'] - 3 * updated_df['Standard_Deviation']

    # Plot the control chart
    plt.figure(figsize=(12, 6))
    plt.plot(
        updated_df['SKU'], updated_df['Mean'], marker='o', linestyle='-',
        color='b', label='Mean'
    )
    plt.fill_between(
        updated_df['SKU'], updated_df['LCL'], updated_df['UCL'], color='lightgrey',
        alpha=0.7, label='Control Limits'
    )
    plt.axhline(
        y=updated_df['LSL'].iloc[0], color='orange', linestyle='--',
        label='Lower Specification Limit (LSL)'
    )
    plt.axhline(
        y=updated_df['USL'].iloc[0], color='purple', linestyle='--',
        label='Upper Specification Limit (USL)'
    )

    plt.title('Control Chart with LSL, USL, UCL, LCL, and mean')
    plt.xlabel('SKU')
    plt.ylabel('Mean/Average Weight')
    plt.legend()
    plt.grid(True)
    # Get the current timestamp and format it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create the directory if it doesn't exist
    output_dir = Path("visuals")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Save the plot with the timestamp in the filename
    filename = output_dir / f"control_chart_{timestamp}.png"
    # Save the generated image in the directory specified above
    plt.savefig(filename)
    if not AUTO_RUN:
        plt.show()

