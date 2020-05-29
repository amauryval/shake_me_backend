import pandas as pd
import geopandas as gpd

import grequests
import itertools

from shake_me_backend.core.time_helper import DatesToMonthDates


class ImportUsgsEarthquakeData:

    _URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}&minlatitude={min_lat}&maxlatitude={max_lat}&minlongitude={min_lng}&maxlongitude={max_lng}"

    __mag_category_mapping = {
        'great': [8, 9999],
        'major': [7, 8],
        'strong': [6, 7],
        'moderate': [5, 6],
        'light': [4, 5],
        'minor': [0, 4],
    }
    _FIELDS_PROPERTIES_TO_KEEP = ['mag', 'time', 'place', 'magType', "x", "y"]

    def __init__(self, start_date, end_date, min_lat, max_lat, min_lng, max_lng, output_csv=None):

        self._start_date = start_date
        self._end_date = end_date
        self._min_lat = min_lat
        self._max_lat = max_lat
        self._min_lng = min_lng
        self._max_lng = max_lng
        self._output_csv = output_csv

        self._get_dates_to_request()
        self._prepare_requests()
        self._query_requests()
        self._get_data()
        self._clean_data()

    def map_jsondata(self):
        return self._data.to_dict(orient="records")

    def chart_jsondata(self):
        chart_data = self._data[["place", "mag_cat"]]
        # chart_data = chart_data.astype({
        #     'place': 'category',
        #     'mag_cat': 'category'
        # })
        chart_data_build = chart_data.groupby(['place', 'mag_cat']).size().reset_index(name='count')
        chart_data_build = chart_data_build.set_index(["place", "mag_cat"]).unstack('mag_cat')
        chart_data_build.columns = chart_data_build.columns.droplevel(0).rename('')
        # chart_data_build.set_index("place", inplace=True)
        chart_data_build = chart_data_build.fillna(value=0)
        chart_data_build = chart_data_build.astype(int)
        chart_data_build = chart_data_build.reset_index()
        return chart_data_build.to_dict(orient="records")

    def _get_dates_to_request(self):

        self._dates_to_request = DatesToMonthDates(
            self._start_date,
            self._end_date
        ).run()
        # get min and max date
        self._dates_to_request = [(self._dates_to_request[0][0], self._dates_to_request[-1][-1])]

    def _prepare_requests(self):
        self._requests = [
            grequests.get(
                self._URL.format(
                    start_date=start_date,
                    end_date=end_date,
                    min_lat=self._min_lat,
                    max_lat=self._max_lat,
                    min_lng=self._min_lng,
                    max_lng=self._max_lng,
                )
            )
            for start_date, end_date in self._dates_to_request
        ]

    def _query_requests(self):
        #TODO Test if response == 200
        self._requests = grequests.map(self._requests)

    def _get_data(self):
        self._data = gpd.GeoDataFrame.from_features(
            list(
                itertools.chain.from_iterable([
                    query.json()['features']
                    for query in self._requests
                ])
            )
        )

    def _clean_data(self):

        self._data["x"] = self._data.geometry.x
        self._data["y"] = self._data.geometry.y
        self._data = self._data[self._FIELDS_PROPERTIES_TO_KEEP]
        self._data = self._data.sort_values(by='time', ascending=True)
        self._data['time'] = self._data['time'].apply(lambda x: pd.to_datetime(x // 10**3, unit="s").strftime("%Y-%m-%d"))
        self._data['mag_cat'] = self._data['mag'].apply(lambda feature: next((cat_title for cat_title, interval in self.__mag_category_mapping.items() if interval[0] <= feature < interval[-1]), 'unknown'))
        self._data = self._data.fillna(value="Unknown")






if __name__ == '__main__':

    start_date = "2000-01-06"
    end_date = "2001-01-09"
    min_lat = 39.095963
    min_lng = -10.063477
    max_lat = 53.265213
    max_lng = 26.477051


    data = ImportUsgsEarthquakeData(start_date, end_date, min_lat , max_lat , min_lng , max_lng)
    map_data = data.map_jsondata()
    chart_data = data.chart_jsondata()
    print('aa')