from logger import logger
from pushover import Pushover
from derozap import Derozap

STATE_FILE = 'zappy_state.json'

def main():
    def handle_zap_status(zap_status):
        if isinstance(zap_status, bool):
            if zap_status:
                p.send_notification(dz.ZAPPED_ACK_MESSAGE)
            else:
                p.send_notification(dz.NOT_ZAPPED_ACK_MESSAGE, priority=-2)
        else:
            p.send_notification(zap_status, priority=-1, is_log=True)

    p = Pushover()
    dz = Derozap()

    handle_zap_status(dz.get_zap_status())

if __name__ == '__main__':
    main()