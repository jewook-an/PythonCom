"""
Get CO2 emission data from the UK CarbonIntensity API
"""

from datetime import date

import requests
import traceback

BASE_URL = "https://api.carbonintensity.org.uk/intensity"

# print(__name__)

# Emission in the last half hour
def fetch_last_half_hour() -> str:
    last_half_hour = requests.get(BASE_URL, timeout=10).json()["data"][0]
    return last_half_hour["intensity"]["actual"]


# Emissions in a specific date range
def fetch_from_to(start, end) -> list:
    try:
        testlist = []
        response = requests.get(f"{BASE_URL}/{start}/{end}", timeout=10)
        # print(f"response.status_code :", response.status_code)
        if (response.status_code == 200):
            testlist = response.json()["data"]
        else:
            print(f"Error :", response.json().get("error"))
        return testlist
    except:
        traceback_message = traceback.format_exc()
        print(f"traceback_message :", traceback_message)

if __name__ == "__main__":
    for entry in fetch_from_to(start=date(2025, 1, 9), end=date(2025, 1, 10)):
        print("from {from} to {to}: {intensity[actual]}".format(**entry))
    print(f"{fetch_last_half_hour() = }")