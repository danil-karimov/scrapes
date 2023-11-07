import json

import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_links(search_text): # to get links from common list
    ua = fake_useragent.UserAgent() # create variable for UA
    res = requests.get(
        url=f"https://hh.ru/search/vacancy?from=suggest_post&ored_clusters=true&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113&text={search_text}&page=1",
        headers={"user-agent": ua.random}
    ) # create variable for request and to write headers = UA random

    if res.status_code != 200: # condition for error
        return
    soup = BeautifulSoup(res.content, "lxml") # to parse content
    try:
        page_count = int(soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return
    for page in range(page_count):
        try:
            res = requests.get(
                url=f"https://hh.ru/search/vacancy?from=suggest_post&ored_clusters=true&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113&text={search_text}&page={page}",
                headers={"user-agent": ua.random}
            )
            if res.status_code != 200:
                continue
            soup = BeautifulSoup(res.content, 'lxml')
            for a in soup.find_all('a', attrs={'class': 'serp-item__title'}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"e")
        time.sleep(1)
    """
    1) to go through the structure 
    2) to get a text of page
    3) to convert in INT
    """

def get_vacancy(link):
    ua = fake_useragent.UserAgent()
    res = requests.get(
        url = link,
        headers={"user-agent": ua.random}
    )
    if res.status_code != 200: # condition for error
        return
    soup = BeautifulSoup(res.content, 'lxml')
    try:
        vac_title = soup.find('div', attrs={'class': 'vacancy-title'}).text.replace('\xa0', '')
    except:
        vac_title = ""
    try:
        salary = soup.find('span', attrs={'class': 'bloko-header-section-2_lite'}).text.replace('\xa0', '')
    except:
        salary = ""
    try:
        company = soup.find('span', attrs={'class': 'vacancy-company-name'}).text.replace('\xa0', ' ')
    except:
        company = ""
    try:
        tasks = soup.find('div', attrs={'class': 'g-user-content'}).text
    except:
        tasks = ""
    vacancy = {
        'vac_title': vac_title,
        'salary': salary,
        'company': company,
        'tasks': tasks
    }
    return vacancy


def read_json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_to_excel(data, filename):
    df = pd.DataFrame([data])  # Convert the dictionary to a DataFrame (inside a list to make it a single row)
    df.to_excel(filename, index=False, engine='openpyxl')
'''
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, engine='openpyxl')
'''
if __name__ == "__main__":
    search_text = "Python"  # Replace with your desired search
    data = []
    counter = 0

    for a in get_links(search_text):
        if counter >= 10:
            break
        data.append(get_vacancy(a))
        time.sleep(1)
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
'''
    json_data = read_json_from_file('/Users/danil/Yandex.Disk.localized/Big data education/mcb_reserve/vacancies.json')
    vac_title = json_data.get('vac_title', 'n/a')
    salary = json_data.get('salary', 'n/a')
    company = json_data.get('company', 'n/a')
    tasks = json_data.get('tasks', 'n/a')

    # Create a dictionary from the extracted fields
    parsed_data = {
        'Vacancy Title': vac_title,
        'Salary': salary,
        'Company': company,
        'Tasks': tasks
    }
    print(parsed_data)
    # Save the parsed data to an Excel file
    #save_to_excel(parsed_data, 'hh_parsed_data.xlsx')  # The data will be saved in 'parsed_data.xlsx'

'''