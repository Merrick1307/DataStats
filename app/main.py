import sys

from DataStats.app.automation import auto
from DataStats.app.manual_run import do_analysis
from DataStats.app.core import logger


def run_analysis(mode):
    """
    Run analysis based on the specified mode.

    This function executes different analysis routines
    depending on the provided mode. It can run the
    analysis in default mode, automatically on a weekly
    schedule, or manually on user demand.

    Parameters:
    mode (str): The mode in which to run the analysis.
    Possible values are:
                - 'default': Runs the default analysis.
                - 'auto': Sets the analysis to run automatically
                  on a weekly schedule.
                - 'manual': Sets the analysis to run manually on
                  user demand.

    Returns:
    None

    Logs:
    - Info: Logs the selected mode and its effect.
    - Debug: Logs an unknown mode and usage instructions.

    Example:
    >>> run_analysis('default')
    >>> run_analysis('auto')
    >>> run_analysis('manual')

    """
    if mode.lower() == 'default':
        do_analysis()
    elif mode.lower() == 'auto':
        auto.auto_run()
        logger.info("Set to run analysis automatically on a weekly schedule")
    elif mode == 'manual':
        logger.info("Set to run analysis manually on user demand")
    else:
        logger.debug(f"Unknown mode: {mode}")
        logger.info("Usage: python main.py [default|auto|manual]")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_mode = sys.argv[1]
    else:
        run_mode = 'default'

    run_analysis(run_mode)