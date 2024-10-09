from logger import logger
from helpers.pushover import Pushover
from state_machine import StateMachine

WARN_MSG = "Reminder: you haven't zapped yet today!"

def warn():
    """
        This will send a Warning Pushover notification if not yet zapped today.
        Cron will trigger this script daily at 9pm.
    """

    p = Pushover()
    sm = StateMachine()

    if not sm.zapped_today:
        p.send_notification(WARN_MSG)
    else:
        logger.debug("Zapped already. Skip warning.")

if __name__ == '__main__':
    warn()