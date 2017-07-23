import pandas as pd
import json
from Parkrun.fetch import fetch_run, fetch_urls_from_courses, fetch_all_course_names, fetch_runs
from Parkrun.util import generate_urls
from Parkrun.extract import get_running_percentile, process_agecats

AMT_COURSES = 10
CSV_FILE_NAME = 'running_data.json'
JSON_FILE_NAME = 'running_data.json'


def append_to_csv(data):
    with open(CSV_FILE_NAME, 'a') as f:
        pd.DataFrame(data).to_csv(f, header=False)


if __name__ == '__main__':
    # course_names = pd.DataFrame(fetch_all_course_names())
    # course_names.to_csv('course_names.txt', header=['Course'])
    #
    # course_names = pd.read_csv('course_names.txt')['Course']
    # urls = pd.DataFrame(fetch_urls_from_courses(course_names, verbose=True))
    #
    # urls.to_csv('run_urls.csv')

    # course_data = pd.read_csv('run_urls.csv', index_col=0)
    #
    # # all_data = []
    #
    # for index, row in course_data[120:130].iterrows():
    #     course_name = row['Course name']
    #     number_of_runs = row['Runs']
    #
    #     urls = generate_urls(course_name, number_of_runs)
    #
    #     running_data = fetch_runs(urls, verbose=True)
    #     # all_data.extend(running_data)
    #
    #     with open('fetched_data/rawdata/' + JSON_FILE_NAME + '_' + course_name + '.json', 'w') as f:
    #         json.dump(running_data, f)

    # process_agecats()
    print get_running_percentile(1260, 'SM20-24')
    print("done")
