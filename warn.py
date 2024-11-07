import os
from helpers.logger import setup_logger, logger
from helpers.pushover import Pushover
from helpers.derozap import Derozap
from state_machine import StateMachine

WARN_MSG = "Reminder: you haven't zapped yet today!"

def warn():
    """
        This will send a Warning Pushover notification if not yet zapped today.
        Cron will trigger this script daily at 9pm.
    """

    # get reference to root folder for absolute path of project files
    root = os.path.dirname(__file__)

    setup_logger(root)
    sm = StateMachine(root)
    p = Pushover()
    dz = Derozap()

    if not sm.zapped_today:
        p.send_notification(WARN_MSG + "\n\n" + dz.stats_summary)
    else:
        logger.debug("Zapped already. Skip warning.")

if __name__ == '__main__':
    warn()