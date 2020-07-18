import re
import urllib.parse
import urllib.request
import csv
import json
import pandas as pd


def main():
    csv_input = 'Save/vacancies_tester_Ekb_and_Moscow.csv'
    csv_output = 'Save/vacancies_Tester_Ekb_Msc.csv'
    json_full = 'Save/vacancies_Tester_Ekb_Msc.json'

    csv_input_file = open(csv_input, 'r')
    csv_sheet = csv.reader(csv_input_file, delimiter=';')
    csv_list = []
    for row in csv_sheet:
        csv_list.append(row[0])
    csv_list = csv_list[1:]

    f1 = open(csv_output, 'wt')
    writer = csv.writer(f1, delimiter=';', )
    writer.writerow(('ID вакансии', 'Название вакансии', 'Название компании', 'Описание вакансии', 'Ключевые навыки',
                     'Населённый пункт', 'Ссылка на вакансию'))
    for vacancy_id in csv_list:
        url = 'https://api.hh.ru/vacancies/' + vacancy_id
        print(url)
        f = open(json_full, 'bw')
        request = urllib.request.Request(url)
        request.encoding = "utf-8"
        response = urllib.request.urlopen(request)
        data = response.read()
        f.write(data)
        f.close()

        json_data = open(json_full, encoding="utf-8")
        data_vac = json.load(json_data)
        json_data.close()

        vacancy_id = data_vac['id']
        name = data_vac['name']
        employer_name = data_vac['employer']['name']
        description = data_vac['description']
        key_skills = data_vac["key_skills"]
        area = data_vac['area']['name']
        vacancy_url = url

        description = clean_from_html(description)
        writer.writerow((str(vacancy_id), str(name), str(employer_name), str(description), str(key_skills), str(area),
                         str(vacancy_url)))
    f1.close()


def clean_from_html(raw_html):
    cleanr = re.compile('<.*?>|&.{4};')
    cleantext = re.sub(cleanr, '', str(raw_html))
    return cleantext


main()
