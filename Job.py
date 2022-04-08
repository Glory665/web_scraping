from bs4 import BeautifulSoup as bs
import requests
import json

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
url = 'https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python&clusters=true&ored_clusters=true&enable_snippets=true&page=0&hhtmFrom=vacancy_search_list'
response = requests.get(url, headers=headers)
dom = bs(response.text, 'html.parser')


def max_page():
    mx = 0
    for spans in dom.find_all('a', {'data-qa': 'pager-page'}):
        mx = spans.find('span').text
        mx = int(mx)
    return mx


max_page = max_page()


def collection(pages):
    job_list = []
    for page in range(pages):
        url1 = f'https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list'
        response1 = requests.get(url1, headers=headers)
        dom1 = bs(response1.text, 'html.parser')
        jobs = dom1.find_all('div', {'class': 'vacancy-serp-item'})
        for job in jobs:
            job_data = {}
            job_title = job.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text.strip()
            job_vacancy = job.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.strip()
            job_link = job.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
            job_salary = job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            job_salary_data = {'min': '', 'max': '', 'currency': ''}
            if job_salary is None:
                job_salary_data['min'] = 'None'
                job_salary_data['max'] = 'None'
                job_salary_data['currency'] = 'None'
            else:
                job_salary = job_salary.text.replace("\u202f", '').split()
                if 'от' in job_salary:
                    if 'руб.' in job_salary:
                        job_salary_data['min'] = int(job_salary[1])
                        job_salary_data['max'] = 'None'
                        job_salary_data['currency'] = 'руб.'
                    if 'USD' in job_salary:
                        job_salary_data['min'] = int(job_salary[1])
                        job_salary_data['max'] = 'None'
                        job_salary_data['currency'] = 'USD'
                if 'до' in job_salary:
                    if 'руб.' in job_salary:
                        job_salary_data['min'] = 'None'
                        job_salary_data['max'] = int(job_salary[1])
                        job_salary_data['currency'] = 'руб.'
                    if 'USD' in job_salary:
                        job_salary_data['min'] = 'None'
                        job_salary_data['max'] = int(job_salary[1])
                        job_salary_data['currency'] = 'USD'
                if 'от' not in job_salary and 'до' not in job_salary:
                    if 'руб.' in job_salary:
                        job_salary_data['min'] = int(job_salary[0])
                        job_salary_data['max'] = int(job_salary[2])
                        job_salary_data['currency'] = 'руб.'
                    if 'USD' in job_salary:
                        job_salary_data['min'] = int(job_salary[0])
                        job_salary_data['max'] = int(job_salary[2])
                        job_salary_data['currency'] = 'USD'

            job_data['job_title'] = job_title
            job_data['job_vacancy'] = job_vacancy
            job_data['job_link'] = job_link
            job_data['job_salary'] = job_salary_data
            job_list.append(job_data)
        return job_list


coll = collection(max_page)


def data_to_json(coll):
    with open('coll.json', 'w', encoding='utf-8') as file:
        json.dump(coll, file)


def main():
    data_to_json(coll)


if __name__ == "__main__":
    main()