"""
This is to show simple COVID19 info fetching from worldometers site using lxml
* The main motivation to use lxml in place of bs4 is that it is faster and therefore
more convenient to use in Python web projects (e.g. Django or Flask-based)
"""

from typing import NamedTuple

import requests
from lxml import html


class CovidData(NamedTuple):
    cases: int
    deaths: int
    recovered: int


def covid_stats(url: str = "https://www.worldometers.info/coronavirus/") -> CovidData:
    xpath_str = '//div[@class = "maincounter-number"]/span/text()'
    return CovidData(
        *html.fromstring(requests.get(url, timeout=10).content).xpath(xpath_str)
    )


fmt = """Total COVID-19 cases in the world: {}
Total deaths due to COVID-19 in the world: {}
Total COVID-19 patients recovered in the world: {}"""

print(fmt.format(*covid_stats()))

"""
*covid_stats():
* 연산자는 언팩(unpack) 연산자입니다. covid_stats() 함수가 반환하는 CovidData 객체의 값을 개별 인자로 분리하여 전달합니다.
예를 들어, covid_stats()가 (1000000, 50000, 900000)을 반환하면, *covid_stats()는 1000000, 50000, 900000으로 변환됩니다.

fmt.format(...) 메서드는 fmt 문자열의 {} 자리 표시자에 인자를 삽입합니다. *covid_stats()로 전달된 값들이 {}에 순서대로 들어갑니다.
"""