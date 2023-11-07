# Import required libraries
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pandas as pd
import fake_useragent
import requests


# Function to fetch a single webpage and return the product URLs
'''
Эта функция принимает номер страницы i, заголовки headers, прокси proxies, и объект 
для генерации User-Agent ua. Она возвращает список URL продуктов с данной страницы
'''
def fetch_page(i, headers, proxies, ua):
    # Make HTTP request to the webpage
    res = requests.get(
        f'https://lalafo.kg/?page={i}',
        headers=headers,
        proxies=proxies
    )
    print(f"Processing page {i}")
    # Parse the HTML content
    soup = BeautifulSoup(res.content, 'lxml')
    # Find all product links on the page
    a_tag = soup.find_all('a', attrs={'class': 'adTile-mainInfo-link'})
    # Return the list of product URLs
    return [f"https://lalafo.kg{link.get('href')}" for link in a_tag]


# Function to fetch product details via API
'''
Эта функция принимает id_card продукта, заголовки и прокси, и возвращает словарь с деталями продукта
'''
def fetch_api_details(id_card, headers, proxies):
    print(f"Processing id_card {id_card}")
    # Make HTTP request to the API
    res = requests.get(
        f'https://lalafo.kg/api/search/v3/feed/details/{id_card}',
        headers=headers,
        proxies=proxies
    )
    # If the request is successful, parse the JSON response
    if res.status_code == 200:
        data_page = res.json()
        user_data = data_page['user']

        # Create a vars for dictionary
        try:
            city = data_page['city']
        except:
            city = ''
        try:
            user_name = user_data['username']
        except:
            user_name = ''
        try:
            mobile_phone = data_page['mobile']
        except:
            mobile_phone = ''
        try:
            hide_phone = data_page['hide_phone']
        except:
            hide_phone = ''
        try:
            email = data_page['email']
        except:
            email = ''
        try:
            pro = user_data['pro']
        except:
            pro = ''
        try:
            company_name = user_data['company_name']
        except:
            company_name = ''
        # Return a dictionary containing relevant product details
        return {
            'city': city,
            'user_name': user_name,
            'mobile_phone': mobile_phone,
            'hide_phone': hide_phone,
            'email': email,
            'pro':pro,
            'company_name': company_name
        }


# Main function
# Тут начинается основная логика программы.
def main():
    # HTTP headers and proxy settings
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
    }

    # Initialize fake user agent
    ua = fake_useragent.UserAgent()

    # Fetch all product URLs using concurrent threads
    links = []
    '''
    Параллельное получение URL продуктов
    Здесь используется ThreadPoolExecutor для параллельного выполнения функции
    fetch_page. Lambda-функция lambda i: fetch_page(i, headers, proxies, ua) 
    просто оборачивает fetch_page, чтобы можно было передать дополнительные параметры
    '''
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda i: fetch_page(i, headers, proxies, ua), range(1000000)) # по сути это генератор значений i которые потом идут в функцию
    for result in results:
        links.extend(result)
        '''
        Метод extend() является методом списка в Python. В данном контексте links — это список, и метод extend() 
        используется для добавления всех элементов из списка result в список links
        '''

    # Fetch product details for each URL using concurrent threads
    contact_list_dict = []
    with ThreadPoolExecutor() as executor:
        id_card_list = [link.split('-')[-1] for link in links]
        api_results = executor.map(lambda id_card: fetch_api_details(id_card, headers, proxies), id_card_list) # это итератор и в нем временно хранится инфа
    for api_result in api_results:
        if api_result:
            contact_list_dict.append(api_result)
    '''
    Lambda-функция в executor.map() просто позволяет передать параметры в fetch_page и fetch_api_details 
    в контексте многопоточного выполнения. Она принимает один аргумент (i или id_card) и вызывает 
    соответствующую функцию с этим аргументом и дополнительными параметрами.
    '''

    # Convert the list of dictionaries to a DataFrame and save to Excel
    df = pd.DataFrame(contact_list_dict)
    # df.to_excel('lalafo_contacts.xlsx', index=False)
    df.drop_duplicates(subset=['mobile_phone', 'email'], inplace=True)
    df['mobile_phone'] = df['mobile_phone'].astype(str).apply(lambda x: x.split('.')[0])
    df.to_excel('unique_contacts.xlsx', index=False)
    df.to_csv('CSV_unique_contacts.csv', index=False)
    print('All data got successfully')


# Entry point of the script
if __name__ == "__main__":
    main()

