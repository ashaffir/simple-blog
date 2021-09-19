"""Users utilities
"""
import threading
import logging
import json
import requests
from tenacity import retry
from datetime import datetime
from django.conf import settings
from tenacity.wait import wait_exponential

logger = logging.getLogger(__file__)


class EnrichUser(threading.Thread):
    """Enrich user profile with IP geolocaiton information and holiday information when relevant"""

    def __init__(self, user):
        self.user = user
        threading.Thread.__init__(self)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def run(self):
        """Executing the calls to the AbstractAPI API"""
        try:
            url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.IP_GEOLOCATION_API}"
            response = requests.get(url)
            if response.status_code == 200:
                info = json.loads(response.content)
                ip_address, country_code = info["ip_address"], info["country_code"]
                self.user.ip_address = ip_address

                now = datetime.now()
                day = now.day
                month = now.month
                year = now.year
                url = f"https://holidays.abstractapi.com/v1/?api_key={settings.HOLIDAYS_API}&country={country_code}&year={year}&month={month}&day={day}"
                response = requests.get(url)
                if response.status_code == 200:
                    content = response.content
                    content_list = json.loads(content)
                    if len(content_list) > 0:
                        self.user.holiday = content_list[0]

                self.user.save()
                logger.info(f"Successful signup by {self.user}")
        except Exception as e:
            logger.error(
                f"Failed getting information from the Abstractapi website {e}. Retrying...  "
            )
            return False
