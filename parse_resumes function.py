import requests
from bs4 import BeautifulSoup
import csv
import re


def parse_resumes(search_text):
    # create a csv file and write headers
    with open(f'{search_text}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Specialization', 'Salary', 'Age', 'Employment(Занятость)', 
                         'Work schedule', 'Experience_years', 'Experience_month', 'Citizenship', 'Sex'])

    # get the number of pages to parse
    url = f'https://hh.kz/search/resume?text={search_text}&order_by=relevance&clusters=true&area=1609&no_magic=true&search_period=30&items_on_page=50'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        page_count = int(soup.select('.bloko-button-group a')[-1].text)
    except IndexError:
        page_count = 1

    # loop through all the pages and parse the data
    for page in range(0, min(page_count, 10)):
        url = f'https://hh.kz/search/resume?text={search_text}&order_by=relevance&clusters=true&area=1609&no_magic=true&search_period=30&items_on_page=50&page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        resumes = soup.select('.resume-search-item__name a')

        # loop through each resume and parse the details from the individual page
        for resume in resumes:
            resume_url = resume['href']
            response = requests.get(resume_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.select_one('h1[data-qa="resume-block-title"]').text
            specialization = soup.select_one('div[data-qa="resume-block-specialization"] a').text
            salary = soup.select_one('span[data-qa="resume-block-salary"]').text.strip()
            if not salary:
                salary = 'NaN'
            age = soup.select_one('div[data-qa="resume-personal-age"] span').text
            if not age:
                age = 'NaN'
            employment = soup.select_one('span[data-qa="resume-block-employment-type"] + span').text
            work_schedule = soup.select_one('span[data-qa="resume-block-schedule-type"] + span').text
            experience = soup.select_one('span[data-qa="resume-block-experience"] + span').text
            experience_years, experience_month = re.findall(r'\d+', experience)
            citizenship = soup.select_one('span[data-qa="resume-personal-country"] + span').text
            sex = soup.select_one('div[data-qa="resume-personal-gender"] span')['class'][1] == 'ic-male'

            # write the details to the csv file
            with open(f'{search_text}.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([title, specialization, salary, age, employment, 
                                 work_schedule, experience_years, experience_month, citizenship, sex])
    with open(file_name, 'w', encoding='UTF8', newline='') as csv_file:
        fieldnames = ['Title', 'Specialization', 'Salary', 'Age', 'Employment',
                      'Work schedule', 'Experience years', 'Experience month', 'Citizenship', 'Sex']
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)

        for resume in resumes:
            writer.writerow(resume)

    return file_name                                 
