
import logging
from datetime import timedelta
import voluptuous as vol
import requests
import pandas as pd
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "AFAD Son Deprem"
SCAN_INTERVAL = timedelta(minutes=1)

CONF_MIN_MAGNITUDE = "min_magnitude"

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_MIN_MAGNITUDE, default=3.5): vol.Coerce(float),
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    min_magnitude = config.get(CONF_MIN_MAGNITUDE)
    add_entities([AfadEarthquakeSensor(name, min_magnitude)], True)

class AfadQuakeSensor(SensorEntity):
    def __init__(self, min_magnitude):
        self._attr_name = "AFAD Son Deprem"
        self._attr_unique_id = "afad_son_deprem"
        self._attr_extra_state_attributes = {}
        self._attr_state = 0.0
        self.min_magnitude = min_magnitude
        
    def update(self):
        _LOGGER.info("AFAD verisi güncelleniyor...")
        url = "https://deprem.afad.gov.tr/last-earthquakes.html"
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "tr,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "f5avraaaaaaaaaaaaaaaa_session_=HJLNJPPDHLGOOGHIDFHIHFCMABPMBFFNBMFOLGMLPLCKLKIKIFHCDPKKODJLMMKAFLADHEAOMOHFODOGJKJABAFBLKOFKPBHPLMKBIGAEIKPDCMCJIENIPIHDBCPONCA; TS01c656ee=013cc8852f9a4acdf7f81348f8417e9df4de846ff1597cce48620386b046e1fc7a544ac818914c9828d4b415ce6adf95381fda0fa96ef0b1b29ce40f919ffb2e9880f135b6; _gid=GA1.3.1675374035.1745596179; _gat_gtag_UA_81499834_3=1; _ga=GA1.1.1508943929.1745596179; _ga_SS9CC6715D=GS1.1.1745596178.1.0.1745596181.0.0.0",
        "DNT": "1",
        "Host": "deprem.afad.gov.tr",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                _LOGGER.error("AFAD sayfası alınamadı (%s)", response.status_code)
                return

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="content-table")
            if not table or not table.tbody:
                _LOGGER.error("AFAD tablosu bulunamadı.")
                return

            rows = table.tbody.find_all("tr")
            data = []
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 7:
                    record = [cell.get_text(strip=True) for cell in cells[:7]]
                    try:
                        date_val = datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S")
                        data.append(record)
                    except:
                        continue

            df = pd.DataFrame(data, columns=["Tarih", "Enlem", "Boylam", "Derinlik", "Tip", "Büyüklük", "Yer"])
            df["Büyüklük"] = pd.to_numeric(df["Büyüklük"], errors="coerce")
            df_filtered = df[df["Büyüklük"] >= self.min_magnitude].reset_index(drop=True)

            if df_filtered.empty:
                _LOGGER.warning("Filtreye uygun deprem verisi yok. %s" , self.min_magnitude)
                return

            quake = df_filtered.iloc[0]
            
            _LOGGER.warning("Son deprem büyüklüğü: %s", quake["Büyüklük"])
            
            map_link = f"https://www.google.com/maps?q={quake['Enlem']},{quake['Boylam']}"
            self._attr_state = quake["Büyüklük"]  # Ana değer olarak büyüklük
            self._attr_native_value = quake["Büyüklük"]  # Ana değer olarak büyüklük
            self._attr_extra_state_attributes = {
                "buyukluk": quake["Büyüklük"], 
                "tarih": quake["Tarih"],
                "enlem": quake["Enlem"],
                "boylam": quake["Boylam"],
                "derinlik": quake["Derinlik"],
                "tip": quake["Tip"],
                "yer": quake["Yer"],
                "harita": map_link
            }

        except Exception as e:
            _LOGGER.error("AFAD verisi çekilirken hata oluştu: %s", e)
