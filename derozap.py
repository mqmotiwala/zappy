import requests
import os
from dotenv import load_dotenv
from logger import logger
from bs4 import BeautifulSoup

class Derozap:
    ZAPPED_DERO_ZAP_TAG_TEXT = 'You got zapped today!'
    NOT_ZAPPED_DERO_ZAP_TAG_TEXT = 'You have not yet been zapped today.'

    ZAPPED_ACK_MESSAGE = 'Zapped!'
    NOT_ZAPPED_ACK_MESSAGE = 'Not yet zapped.'

    ZAP_URL = 'https://www.derozap.com/'
    ZAP_PARAMS = {'s': 'login'}

    def __init__(self):
        load_dotenv()

        self.email = os.getenv('DEROZAP_EMAIL')
        self.password = os.getenv('DEROZAP_PASSWORD')
        self.form_data = {'email_login': self.email, 'password_login': self.password}

    def get_zap_status(self):
        """
        Make a request to the Derozap website and parse returned HTML for current zap message.

        Returns:
            Bool | str: Zapped status as boolean value, or error_msg as str if an error occurs.
        """
        try:
            response = requests.post(self.ZAP_URL, params=self.ZAP_PARAMS, data=self.form_data)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            p_tag = soup.find('p', class_='zappedToday')

            if p_tag:
                zap_message = p_tag.get_text(strip=True)

                if zap_message == self.ZAPPED_DERO_ZAP_TAG_TEXT:
                    logger.info(self.ZAPPED_ACK_MESSAGE)
                    return True

                elif zap_message == self.NOT_ZAPPED_DERO_ZAP_TAG_TEXT:
                    logger.info(self.NOT_ZAPPED_ACK_MESSAGE)

                    return False
                else:
                    return zap_message
            else:
                error_msg = 'Zap status paragraph tag not found on the page.'
                logger.error(error_msg)

                return error_msg

        except requests.exceptions.RequestException as e:
            error_msg = "An error occurred while making a request to Derozap"
            logger.exception(error_msg)

            return (f"{error_msg}: {e}")