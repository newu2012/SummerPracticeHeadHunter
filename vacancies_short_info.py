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
    page = 10
    url = 'https://api.hh.ru/vacancies?area=' + area_id + '&search_field=name&text=' + job + '&per_page=100'

    file = json_file
    if (job == "tester") & (area_id == "1261"):
        file = json_tester

    get_request(csv_file, json_file, file, page, per_page, url)


def get_request(csv_file, json_file, file, page, per_page, url):
    f1 = open(csv_file, 'wt')
    writer1 = csv.writer(f1, delimiter=';')
    writer1.writerow(('Название вакансии', 'Название компании', 'Местонахождение', 'Обязанности', 'Требования',
                      'Ключевые навыки', 'Ссылка на вакансию'))

    i = 1
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
        i = i + 1

        json_data = open(file, encoding="utf-8")
        data_vac = json.load(json_data)
        json_data.close()

        #преобразуем json в csv
        n = 0
        found = int(data_vac['found'])
        if found > 100:
            if found - (i - 1) * per_page > per_page:
                vac_per_page = per_page
            else:
                vac_per_page = found - (i - 1) * per_page
                i = page + 1
        else:
            vac_per_page = found
            i = page + 1

        while n < vac_per_page:
            name = data_vac['items'][n]['name']
            requirement = data_vac['items'][n]['snippet']['requirement']
            responsibility = data_vac['items'][n]['snippet']['responsibility']
            employer_name = data_vac['items'][n]['employer']['name']
            key_skills = "None"
            employer_area = data_vac['items'][n]['area']['name']
            vacancy_url = data_vac['items'][n]['alternate_url']
            writer1.writerow((str(name), str(employer_name), str(employer_area), str(requirement), str(responsibility), str(key_skills), str(vacancy_url)))
            print(str(n) + ". " + name, "(" + employer_name + ")")
            n = n + 1

    f1.close()


main()
