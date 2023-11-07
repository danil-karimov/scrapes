import pandas as pd
import requests
from bs4 import BeautifulSoup
import fake_useragent
import re
from concurrent.futures import ThreadPoolExecutor


def get_links ():
    ua = fake_useragent.UserAgent()
    headers = {'user-agent': ua.random}
    proxies = {
        'http': 'http://JpEYgz:fEyr3C@45.137.85.192:8000'
    }
    links = []
    for i in range(102):
        res = requests.get(
            url=f'https://doska.kg/cat/page={i}',
            headers=headers,
            proxies=proxies
        )
        if res.status_code != 200:
            return 'Error'

        soup = BeautifulSoup(res.content, 'lxml')
        card_links = soup.find_all('a', attrs={'class': 'title_url'})
        print(f"Links from page {i} has been parsed")
        for link in card_links:
            links_info = f"https://doska.kg{link.get('href')}"
            links.append(links_info)
    return links


def collect_info(url):
    ua = fake_useragent.UserAgent()
    headers = {'user-agent': ua.random}
    proxies = {
        'http': 'http://JpEYgz:fEyr3C@45.137.85.192:8000'
    }
    res = requests.get(
        url=url,
        headers=headers,
        proxies=proxies
    )
    soup = BeautifulSoup(res.content, 'lxml')
    city = soup.find('a', attrs={'title': 'Еще в этом регионе'}).text
    description = soup.find('span', attrs={'itemprop': 'description'}).text.replace('\n', '').replace('\r', '').replace(' ', '').replace('+', '')
    # phone_pattern = r'\b(0\d{3}[-\s]?\d{2}[-\s]?\d{2}[-\s]?\d{2})\b|\b(\+\s?996[-\s]?\d{3}[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3})\b'
    phone_pattern = r'(0\d{3}\d{2}\d{2}\d{2})|(996\d{3}\d{2}\d{2}\d{2})|(0996\d{3}\d{2}\d{2}\d{2})'
    phone_numbers = re.findall(phone_pattern, description)
    filtered_num = [num for sublist in phone_numbers for num in sublist if num]

    info = {
        'city': city,
        # 'description': description,
        'phone_num': filtered_num
    }
    return info


# def main():
#     url_list = get_links()
#     data_results_list = []
#     with ThreadPoolExecutor() as executor:
#         data_results = executor.map([collect_info(url), url_list])
#     for data in data_results:
#         if data:
#             data_results_list.append(data)
#     return print(data_results_list)

def main():
    url_list = get_links()
    print(f"URL List: {url_list}")  # Debugging line
    data_results_list = []

    if url_list != 'Error':
        with ThreadPoolExecutor() as executor:
            data_results = list(executor.map(collect_info, url_list))

        print(f"Data Results: {data_results}")  # Debugging line

        for data in data_results:
            if data:
                data_results_list.append(data)

        print(data_results_list)  # Debugging line

    df = pd.DataFrame(data_results_list)
    df.to_excel('doska_kg_data.xlsx', index=False)

if __name__ == '__main__':
    main()

"""
0996220290930
996220290930
+9962202909930
"""