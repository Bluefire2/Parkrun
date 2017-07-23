import os

import pandas as pd


def get_course(url):
    return url.split('/')[-4]


def generate_urls(course_name, number_of_runs):
    base_url = 'http://www.parkrun.org.uk/%s/results/weeklyresults/?runSeqNumber=' % course_name
    return [base_url + str(i) for i in range(1, number_of_runs)]


def to_h(t):
    if len(t) == 5:
        return '00:' + t
    elif len(t) == 7:
        return '0' + t
    else:
        return t


def time_to_secs(t):
    return (t.hour * 60 + t.minute) * 60 + t.second


def update_json_file(filename, data):
    if os.path.isfile(filename):
        with open(filename) as f:
            old_data = pd.read_json(f)
            new_data = pd.concat([old_data, data])
    else:
        new_data = data

    with open(filename, 'w+') as f:
        try:
            new_data.to_json(f, orient='records')
        except AttributeError:
            print 'e'


def percentile(series, value):
    return (series.sort_values().reset_index()['Time'].searchsorted(value) / float(len(series)) * 100)[0]