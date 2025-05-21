from homeassistant.helpers.entity import Entity
import requests
from bs4 import BeautifulSoup
import logging

_LOGGER = logging.getLogger(__name__)

URL = "https://deprem.afad.gov.tr/last-earthquakes.html"

def is_in_marmara_by_coords(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return 40.0 <= lat <= 42.2 and 26.0 <= lon <= 30.5
    except:
        return False

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([AFADMarmaraSensor()], True)

class AFADMarmaraSensor(Entity):
    def __init__(self):
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Marmara Depremi"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        try:
            response = requests.get(URL, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.select("table.content-table tbody tr")

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 8:
                    continue

                tarih = cols[0].text.strip()
                enlem = cols[1].text.strip()
                boylam = cols[2].text.strip()
                buyukluk = float(cols[5].text.strip())
                yer = cols[6].text.strip()
                detay_link = cols[7].find("a")["href"].strip()

                if is_in_marmara_by_coords(enlem, boylam) and buyukluk >= 4.0:
                    self._state = buyukluk
                    self._attributes = {
                        "yer": yer,
                        "tarih": tarih,
                        "enlem": enlem,
                        "boylam": boylam,
                        "buyukluk": buyukluk,
                        "detay_link": detay_link
                    }
                    break
        except Exception as e:
            _LOGGER.error("AFAD verileri alınırken hata: %s", e)
