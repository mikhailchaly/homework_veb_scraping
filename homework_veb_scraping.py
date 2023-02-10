import requests
import lxml
from fake_headers import Headers
from bs4 import BeautifulSoup
import time
import re
import json

def get_headers():
    headers = Headers(browser="firefox", os="win")
    return headers.generate()

def search_vacanciy():
    count_vacanciy = []
    list_vacanciy_url= []
    list_description_vacanciy= []
    dict_vacanciy = {}
    _list_selected_vacancies = []
    list_selected_vacancies = []

    for page in range(0, int(input("сколько страниц парсить? ")) + 1):
        time.sleep(0.5)
        url_main_page = f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}"
        response = requests.get(url_main_page, headers=get_headers())
        #print(response.status_code)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="serp-item")

        for i in data:
            vacanciy_url = i.find("a", class_="serp-item__title").get("href")
            list_vacanciy_url.append(vacanciy_url)


        for vacanciy_url in list_vacanciy_url:
            response_1 = requests.get(vacanciy_url, headers=get_headers())
            #print(response_1.status_code)
            soup_1 = BeautifulSoup(response_1.text, "lxml")

            try:
                _company = soup_1.find("span", class_="vacancy-company-name").find("span").text
                name_company = re.sub(r"ОООHeadHunter::", "", _company)
            except:
                pass

            try:
                city = soup_1.find("a", class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited").find("span").text
            except:
                pass

            try:
                salary = soup_1.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text
            except:
                pass

            try:
                name_vacanciy = soup_1.find("h1", class_="bloko-header-section-1").text
            except:
                pass

            description_vacanciy = soup_1.find("div", class_="l-paddings b-vacancy-desc")

            a = re.findall(r"Django|Flask", str(description_vacanciy), re.I)
            b = re.findall(r"Django|Flask", str(name_vacanciy), re.I)

            if len(a) > 0 or len(b) > 0:
                print(name_vacanciy)
                print(f"найденые ключевые слова: {*a, *b}")
                print(f"ссылка: {vacanciy_url}")
                print(f"компания:", name_company)
                print(salary)
                print(city)
                print()
                count_vacanciy.append(1)
                dict_vacanciy = {name_vacanciy: [vacanciy_url,
                                                 salary.replace('\xa0', ''),
                                                 name_company,
                                                re.sub(r",.+", "", city)
                                                ]}
                _list_selected_vacancies.append(dict_vacanciy)
            list_selected_vacancies = list(filter(None, _list_selected_vacancies))

            with open('selected vacancies.json', 'w') as f:
                json.dump(list_selected_vacancies, f, sort_keys=True, ensure_ascii=False, indent=2)
    print(f"найдено {len(count_vacanciy)} вакансий")

if __name__ == "__main__":
    search_vacanciy()




