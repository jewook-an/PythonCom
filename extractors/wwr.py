from requests import get
from bs4 import BeautifulSoup   #beautifulsoup4

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:  # Check response 200(OK)
        print("Can't request website")
    else:
        print("request website")
        results = []  # for Loop의 job_data가 저장될 곳
        soup = BeautifulSoup(response.text, "html.parser")  # 웹사이트 코드 변환
        jobs = soup.find_all('section', class_="jobs")  # jobs 섹션 검색

        for job_section in jobs:  # jobs: Entity(String X)
            job_posts = (job_section.find_all('li'))  # 'li' 태그 검색
            job_posts.pop(-1)  # 필요없는 마지막 정보 삭제

            for post in job_posts:  # 데이터 Loop
                anchors = post.find_all('a')
                anchor = anchors[1]  # 첫번째 a는 필요없음, 두번째가 필요
                print(anchor[1])
                print(anchor[2])
                link = anchor['href']  # anchor: Dictionary
                company, kind, location = anchor.find_all(
                    'span',
                    class_="company")  # 순서대로 저장 ex) company = List[0]...
                title = anchor.find('span', class_='title')

                job_data = {
                    'link': f"https://weworkremotely.com/{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': title.string.replace(",", " ")
                }

                results.append(job_data)  # results에 저장
        return results  # results 반환