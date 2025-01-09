import sys
import webbrowser

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

if __name__ == "__main__":
    print("Googling.....")

    url = "https://www.google.com/search?q=" + " ".join(sys.argv[1:])
    # url = "https://www.google.com/search?q=Python"

    res = requests.get(url, headers={"UserAgent": UserAgent().random}, timeout=10)

    # res.raise_for_status()
    with open("project1a.html", "wb") as out_file:  # only for knowing the class
        for data in res.iter_content(10000):
            out_file.write(data)

    soup = BeautifulSoup(res.text, "html.parser")
    links = list(soup.select(".eZt8xd"))[:5]

    print(len(links))

    for link in links:
        if link.text == "Maps":
            webbrowser.open(link.get("href"))
        else:
            webbrowser.open(f"https://google.com{link.get('href')}")

"""
1. sys.argv:
    - sys 모듈의 argv는 명령줄 인수 포함 리스트.
    - sys.argv[0]는 실행 중인 스크립트 이름 포함, sys.argv[1:]는 스크립트에 전달된 모든 인수 포함.
        (스크립트 실행 예 : python crawl_google_results.py Python programming)
    - 이 경우, sys.argv는 다음과 같은 리스트가 됩니다:
        (  ['crawl_google_results.py', 'Python', 'programming'])
2. sys.argv[1:]:
    - sys.argv[1:] 는 리스트의 첫 번째 요소(스크립트 이름)를 제외한 나머지 요소들 포함.
    - 위의 예시는 ['Python', 'programming'] 이 된다.
3. " ".join(sys.argv[1:]):
    - join 메서드는 리스트의 요소들을 지정된 문자열(여기서는 공백 " ")로 결합.
    - 따라서 " ".join(sys.argv[1:])는 ['Python', 'programming']을 "Python programming" 문자열 변환.
"""