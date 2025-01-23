import time

import schedule

from DataStats.app import manual_run
from DataStats.app.core import logger
from DataStats.app.core.config import AUTO_RUN


def auto_run():
    if AUTO_RUN:
        # Schedule the job to run every Monday at 8:00 AM
        schedule.every().monday.at("08:00").do(manual_run.do_analysis())

        logger.info("Scheduler started. Press Ctrl+C to exit.")

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    else:
        pass