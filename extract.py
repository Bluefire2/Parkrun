import os

import pandas as pd

from Parkrun.config import AGE_CATEGORIES
from Parkrun.util import to_h, time_to_secs, update_json_file, percentile


def get_running_percentile(value, agecat):
    filename = 'fetched_data/data/' + agecat + '.json'
    df = pd.read_json(filename).groupby('Name').aggregate('min')
    series = df['Time']
    return percentile(series, value)


def process_agecats():
    for filename in os.listdir('fetched_data/rawdata'):
        if filename.endswith('.json'):
            path = os.path.join('fetched_data/rawdata', filename)
            print(path)

            file_data = pd.read_json(path)

            file_data = file_data[~(file_data[['Time', 'Gender', 'Position', 'Age category']].values == '').any(axis=1)]
            file_data['Time'] = file_data['Time'].apply(to_h)
            file_data['Time'] = pd.to_datetime(file_data['Time'], format='%H:%M:%S').dt.time.apply(time_to_secs)
            file_data = file_data.sort_values('Time')

            for cat in AGE_CATEGORIES:
                curr_data = file_data[file_data['Age category'] == cat]

                update_json_file('fetched_data/data/' + cat + '.json', curr_data)

        else:
            continue

            # Index the rows by time
            # Do better runners run more frequently?
