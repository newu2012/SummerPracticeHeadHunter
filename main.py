import urllib.parse
import urllib.request
import csv
import json
import pandas as pd


def main():
    job = "tester"
    area_id = "1261"  # Номер города/области, i.e. 1 - Москва, 1261 - Свердловская область
    json_tester = 'vacanciesCompleted.json'  # В апи hh.ru поиск по специальноси "Тестировщик" в Св. области сломан
    basic_URL = 'https://api.hh.ru/vacancies?area=1261&search_field=name&text=tester&per_page=100'

    json_file = 'jsonFrames/vacancies_' + job + area_id + '.json'
    csv_file = 'csvFrames/vacancies_' + job + area_id + '.csv'
    per_page = 100
    page = 19  # Не больше 19 страниц, если в странице по 100!!! Ограничениие hh.ru
    url = 'https://api.hh.ru/vacancies?area=' + area_id + '&search_field=name&text=' + job + '&per_page=100'

    file = json_file
    if (job == "tester") & (area_id == "1261"):
        file = json_tester

    get_request(json_file, csv_file, file, page, per_page, url)


def get_request(json_file, csv_file, file, page, per_page, url):
    i = 1
    f1 = open(csv_file, 'wt')
    writer = csv.writer(f1, delimiter=';')
    writer.writerow(('ID вакансии', 'Название вакансии'))
    while i <= page:
        print("page=" + str(i))
        f = open(json_file, 'bw')
        new_url = url + '&page=' + str(i)
        request = urllib.request.Request(new_url)
        request.encoding = "utf-8"
        response = urllib.request.urlopen(request)
        data = response.read()
        f.write(data)
        f.close()

        i += parse_vacancies(file, writer, i, page, per_page)
        i = i + 1
    f1.close()


# Парсим вакансии из json в csv
def parse_vacancies(json_file, writer, i, page, per_page):
    json_data = open(json_file, encoding="utf-8")
    data_vac = json.load(json_data)
    json_data.close()

    n = 0
    found = int(data_vac['found'])
    if found > 100:
        if found - i * per_page > per_page:
            vac_per_page = per_page
            if page == 20:
                vac_per_page = 99
        else:
            vac_per_page = found - i * per_page
            i = page + 1
    else:
        vac_per_page = found
        i = page + 1

    while n < vac_per_page:
        vacancy_id = data_vac['items'][n]['id']
        name = data_vac['items'][n]['name']
        writer.writerow((str(vacancy_id), str(name)))
        #print(str(n) + ". " + name, "(" + vacancy_id + ")")
        n += 1
    if i > page:
        return page
    else:
        return 0

main()
