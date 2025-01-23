import os

from dotenv import load_dotenv

# Load the environment variable
load_dotenv()


# Instantiate the required environment variables As Constants
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USERNAME")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
EXCEL_FILE = os.getenv("EXCEL_FILE")
TABLE_NAME = os.getenv("TABLE_NAME")
AUTO_RUN = bool(int(os.getenv("AUTORUN")))
VISUALIZE = bool(int(os.getenv("VISUALIZE")))