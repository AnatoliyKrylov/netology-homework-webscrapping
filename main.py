import requests
import bs4
import fake_headers
import time
import json

vacancy_data = []
json_data = {}
headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get('https://hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=headers_gen.generate())
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')
div_id_list_tags = main_soup.find('div', attrs={'data-qa': 'vacancy-serp__results'})
vacancy_list = div_id_list_tags.find_all(class_='vacancy-serp-item-body')

for vacancy in vacancy_list:
    h3_tag = vacancy.find('h3', class_='bloko-header-section-3')
    vacancy_link = h3_tag.find('a')['href']
    if vacancy.find('span', class_={'bloko-header-section-2'}):
        salary = vacancy.find('span', class_={'bloko-header-section-2'}).text.strip().replace(u"\u202f", '')
    else:
        salary = 'None'
    company = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    time.sleep(0.1)
    vacancy_full = requests.get(vacancy_link, headers=headers_gen.generate())
    vacancy_full_html = vacancy_full.text
    vacancy_full_soup = bs4.BeautifulSoup(vacancy_full_html, 'lxml')
    vacancy_description = vacancy_full_soup.find('div', attrs={'data-qa': 'vacancy-description'})
    if 'django' in vacancy_description.text.lower() and 'flask' in vacancy_description.text.lower():
        vacancy_data.append({'link': vacancy_link, 'salary': salary, 'company': company, 'city': city})

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump({'vacancies': vacancy_data}, f, ensure_ascii=False)
