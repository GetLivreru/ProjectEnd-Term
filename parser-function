import requests
from bs4 import BeautifulSoup

def parse_resumes(search_text):
    url = f"https://hh.kz/search/resume?area=40&clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&text={search_text}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs_list = []

    for job in soup.find_all("div", class_="resume-search-item__name"):
        job_title = job.a.text.strip()
        job_link = job.a.get("href")
        jobs_list.append({"title": job_title, "link": job_link})

    return jobs_list
