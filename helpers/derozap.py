import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from helpers.logger import logger
from datetime import datetime, timedelta
from tabulate import tabulate

class Derozap:
    ZAPPED_DERO_ZAP_TAG_TEXT = 'You got zapped today!'
    NOT_ZAPPED_DERO_ZAP_TAG_TEXT = 'You have not yet been zapped today.'

    ZAPPED_ACK_MESSAGE = 'Zapped!'
    NOT_ZAPPED_ACK_MESSAGE = 'Not yet zapped.'

    ZAP_URL = 'https://www.derozap.com/'
    LOGIN_PARAMS = {'s': 'login'}

    VALID_TIMEFRAMES = ['tw', 'tm', 'ty', 'al']

    DERO_ZAP_START_DATE = datetime(2022, 1, 31)

    def __init__(self):
        load_dotenv()

        self.email = os.getenv('DEROZAP_EMAIL')
        self.password = os.getenv('DEROZAP_PASSWORD')
        self.form_data = {'email_login': self.email, 'password_login': self.password}

        # initialize a session and login
        self.session = requests.Session()
        self.login()

    def login(self):
        """
        Log in to the Derozap website using the provided credentials.
        """
        try:
            response = self.session.post(self.ZAP_URL, params=self.LOGIN_PARAMS, data=self.form_data)
            response.raise_for_status()

            logger.info("Successfully logged in to Derozap.")

        except requests.exceptions.RequestException as e:
            logger.exception("Failed to log in to Derozap.")

            raise Exception(f"Login failed: {e}")

    def get_zap_status(self):
        """
        Make a request to the Derozap website and parse returned HTML for current zap message.

        Returns:
            Bool | str: Zapped status as boolean value, or error_msg as str if an error occurs.
        """
        try:
            response = self.session.get(self.ZAP_URL)
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

    @staticmethod
    def _process_commuter_report(report_text):
        """
        Extracts the first <td> value in the <tbody> section with class "field-number" from the HTML response.

        Args:
            report_text (str): HTML content as a string.

        Returns:
            str: The text content of the first <td class="field-number"> tag within <tbody>.
        """

        soup = BeautifulSoup(report_text, 'html.parser')

        # extract the specific tag which contains the number of zaps in stats report
        return soup.find('table', class_='reportTable reportZapByUser') \
                .find('tbody') \
                .find('td', class_='field-number') \
                .get_text(strip=True) if soup.find('table', class_='reportTable reportZapByUser') \
                .find('tbody') \
                .find('td', class_='field-number') else None

    def _get_zaps_since_date(self, start_date):
        """
        Request a commuter report for zap activity since start_date.
        Request params require the following mandatory key-value pairs:
            's': 'commuter_report',
            'rpid': '1050'

        Args:
            start_date (str)

        Returns:
            str | None: number of zaps since start date as string, or None if error.
        """

        params = {
            'ds': start_date,
            'de': datetime.today().strftime('%m/%d/%Y'),
            's': 'commuter_report',
            'rpid': '1050',
        }

        try:
            response = self.session.get(self.ZAP_URL, params=params)
            response.raise_for_status()
            logger.info(f"Successfully executed commuter report request for zap activity since {start_date}.")

            return Derozap._process_commuter_report(response.text)

        except requests.exceptions.RequestException as e:
            error_msg = f"An error occurred while executing commuter report request for zap activity since {start_date}."
            logger.exception(error_msg)

            return None

    @staticmethod
    def _process_commuter_report(report_text):
        """
        Extracts the first <td> value in the <tbody> section with class "field-number" from the HTML response.

        Args:
            report_text (str): HTML content as a string.

        Returns:
            str: The text content of the first <td class="field-number"> tag within <tbody>.
        """

        soup = BeautifulSoup(report_text, 'html.parser')

        # extract the specific tag which contains the number of zaps in stats report
        return soup.find('table', class_='reportTable reportZapByUser') \
                .find('tbody') \
                .find('td', class_='field-number') \
                .get_text(strip=True) if soup.find('table', class_='reportTable reportZapByUser') \
                .find('tbody') \
                .find('td', class_='field-number') else None

    @property
    def stats_summary(self):
        """
        Generates a summary table of zap activity for different timeframes (This Week, This Month, This Year, All Time)

        Returns:
            str: A formatted plain-text table summarizing the stats for each timeframe.

        Example output:
            This Week   3/4       75%  $45
            This Month  3/6       50%  $45
            This Year   161/311   52%  $2,415
            All Time    541/1011  54%  $8,115
        """

        today = datetime.today()
        start_dates = {
            'This Week': today - timedelta(days=today.weekday() + 1 if today.weekday() < 6 else 0), # starting Sunday
            'This Month': today.replace(day=1),
            'This Year': today.replace(month=1, day=1),
            'All Time': self.DERO_ZAP_START_DATE
        }

        stats = []
        for timeframe, start_date in start_dates.items():
            num_zaps = self._get_zaps_since_date(start_date)
            num_days = (today - start_date).days

            stats_row = (
                timeframe,
                str(num_zaps) + "/" + str(num_days),
                f"{100 * int(num_zaps) / int(num_days):.0f}%",
                f"${15 * int(num_zaps):,.0f}"
            )

            stats.append(stats_row)

        return tabulate(stats, tablefmt="plain")