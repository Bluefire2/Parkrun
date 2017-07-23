from time import sleep

import requests
from bs4 import BeautifulSoup

from Parkrun.config import HEADERS_FOR_HTTP_GET
from Parkrun.util import get_course


def fetch_all_course_names():
    course_names = []
    courses_url = 'http://www.parkrun.org.uk/results/courserecords/'

    response = requests.get(courses_url, headers=HEADERS_FOR_HTTP_GET)
    soup = BeautifulSoup(response.content, 'lxml')
    courses = soup.find('table', id='results').find('tbody').find_all('tr')

    for course_data in courses:
        first_td = course_data.find('td')
        url = first_td.find('a')['href']

        course_names.append(url.split('/')[-2])

    return course_names


def fetch_run(url):
    out = []

    response = requests.get(url, headers=HEADERS_FOR_HTTP_GET)
    soup = BeautifulSoup(response.content, 'lxml')
    runners = soup.find('table', id='results').find_all('tr')

    for runner in runners[1:]:
        runner_data = {}
        cells = [td.text.encode('utf-8') for td in runner.find_all('td')]

        runner_data['Position'] = cells[0]
        runner_data['Name'] = cells[1]
        runner_data['Time'] = cells[2]
        runner_data['Age category'] = cells[3]
        runner_data['Gender'] = cells[5]
        runner_data['Gender position'] = cells[6]
        runner_data['Club'] = cells[7]
        runner_data['Note'] = cells[8]
        runner_data['Total runs'] = cells[9]
        runner_data['Course'] = get_course(url)

        out.append(runner_data)

    return out


def fetch_number_of_runs(course_name):
    url = 'http://www.parkrun.org.uk/%s/results/eventhistory/' % course_name

    response = requests.get(url, headers=HEADERS_FOR_HTTP_GET)
    soup = BeautifulSoup(response.content, 'lxml')
    first_run = soup.find('table', id='results').find('tbody').find('tr')

    # for run in runs:
    #     first_td = run.find('td')
    #     url = first_td.find('a')['href']
    #
    #     print url

    first_td = first_run.find('td')
    url = first_td.find('a')['href']
    number_of_runs = int(url.split('=')[-1])

    return number_of_runs


def fetch_runs(urls, request_limit=float("inf"), pause=0, verbose=False, callback=lambda: None, store_all=True):
    out = []
    i = 0
    total_runs = len(urls)

    for url in urls:
        if i < request_limit:
            try:
                fetched = fetch_run(url)

                if store_all:
                    out.extend(fetched)
                else:
                    callback(fetched)
            except:
                pass  # lol

            i += 1
            sleep(pause)

            if verbose:
                print "{0} runs processed, {1} remaining out of {2}".format(i, total_runs - i, total_runs)
        else:
            break

    if verbose:
        print "All runs processed"

    return out


def fetch_urls_from_courses(courses, request_limit=float("inf"), pause=0, verbose=False):
    out = []
    i = 0
    total_courses = len(courses)

    for course_name in courses:
        if i < request_limit:
            course_data = {}
            number_of_runs = fetch_number_of_runs(course_name)

            course_data['Course name'] = course_name
            course_data['Runs'] = number_of_runs

            out.append(course_data)

            i += 1
            sleep(pause)

            if verbose:
                print "{0} courses processed, {1} remaining out of {2}".format(i, total_courses - i, total_courses)
        else:
            break

    if verbose:
        print "All urls fetched"

    return out
