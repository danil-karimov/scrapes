import time

from bs4 import BeautifulSoup
import pandas as pd
import fake_useragent
import requests
import json


def get_links():
    link_dict = []
    page_count = 0
    for i in range(100):
        res = requests.get(
            url=f'https://lalafo.kg/?page={i}',
            headers={'user-agent': ua.random},
            proxies=proxies
        )
        soup = BeautifulSoup(res.content, 'lxml')
        a_tag = soup.find_all('a', attrs={'class': 'adTile-mainInfo-link'})
        for link in a_tag:
            link_card = f"https://lalafo.kg{link.get('href')}"

            link_dict.append(link_card)
        # time.sleep(1)
        page_count += 1
        print(f"Got a {page_count} pages")
    return link_dict


def get_api(links):
    # links = get_links()
    id_card_dict = []
    contact_list_dict = []
    contact_count = 0
    for id in links:
        id_card = id.split('-')[-1]
        id_card_dict.append(id_card)
    for i in id_card_dict:
        res = requests.get(
            url=f'https://lalafo.kg/api/search/v3/feed/details/{i}',
            headers=headers,
            proxies=proxies
        )
        if res.status_code != 200:
            print("Error")
        data_page = res.json()
        city = data_page['city']
        user_name = data_page['username']
        mobile_phone = data_page['mobile']
        email = data_page['email']

        contact_list = {
            'city': city,
            'user_name': user_name,
            'mobile_phone': mobile_phone,
            'email': email
        }
        contact_list_dict.append(contact_list)
        contact_count += 1
        # time.sleep(1)
        print(f"Got a {contact_count} contacts")


    df = pd.DataFrame(contact_list_dict)
    df.to_excel('lalafo_contacts.xlsx', index=False)

    # for card in links:
    #     res = requests.get(
    #         url=card,
    #         headers={'user-agent': ua.random}
    #     )
    #
    #     soup = BeautifulSoup(res.content, 'lxml')
    #
    #     user_name = soup.find('span', attrs={'class': 'userName-text'}).text
    #     print(user_name)

    print('All data to got successfully')


def main():
    links = get_links()
    get_api(links=links)

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Authorization": "Bearer",
    "country-id": "12",
    "device": "pc",
    "experiment": "novalue",
    "language": "ru_RU",
    "request-id": "react-client_3c8a1d80-190a-4c6d-b777-421b295dd5d2",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "user-hash": "862e72b5-501a-43f7-a851-0d530b709a96",
    "X-Cache-Bypass": "yes"
}


proxies = {
    'http': 'http://JpEYgz:fEyr3C@45.137.85.192:8000'
    #'https': 'https://JpEYgz:fEyr3C@45.137.85.192:8000'
}


ua = fake_useragent.UserAgent()


if __name__ == "__main__":
    main()

