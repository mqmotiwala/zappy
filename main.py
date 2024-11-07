import os
from helpers.pushover import Pushover
from helpers.derozap import Derozap
from helpers.database import Database
from state_machine import StateMachine
from helpers.logger import setup_logger, logger

def main():
    def handle_zap_status(zap_status):
        if isinstance(zap_status, bool):
            if zap_status:
                p.send_notification(dz.ZAPPED_ACK_MESSAGE + "\n\n" + dz.stats_summary)
                sm.update_state(True)
                db.log_zap()
        else:
            p.send_notification(zap_status, priority=-1, is_log=True)

    # get reference to root folder for absolute path of project files
    root = os.path.dirname(__file__)

    setup_logger(root)
    db = Database(root)
    sm = StateMachine(root)
    p = Pushover()
    dz = Derozap()

    if not sm.zapped_today:
        handle_zap_status(dz.get_zap_status())
    else:
        logger.debug("Zapped already. Skip run.")

if __name__ == '__main__':
    main()