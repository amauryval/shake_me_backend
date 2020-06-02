import grequests
import itertools
import geopandas as gpd


class NominatimApi:

    _URL = "https://nominatim.openstreetmap.org/reverse/?format=geojson&lat={lat}&lon={lon}"

    def __init__(self, coords):

        # assert set(coords[0].keys) == set(["lat", "lon", "place"])


        self._coords = coords
        self._prepare_requests()
        self._query_requests()
        self._get_data()

    def data(self):
        return self._data

    def _prepare_requests(self):
        self._requests = [
            grequests.get(
                self._URL.format(
                    lat=coord["lat"],
                    lon=coord["lon"],
                )
            )
            for coord in self._coords
        ]

    def _query_requests(self):
        self._requests = grequests.map(self._requests)

    def _get_data(self):
        # for query in self._requests:
        #     if "features" in query.json():
        #         print(query.json()['features'][0]["properties"]["address"]["country"])

        self._data = gpd.GeoDataFrame.from_features(
            list(
                itertools.chain.from_iterable([
                    query.json()['features']
                    for query in self._requests
                    if "features" in query.json()
                ])
            )
        )

        self._data["lat"] = round(self._data["geometry"].y, 2)
        self._data["lon"] = round(self._data["geometry"].x, 2)
        self._data["country"] = self._data["address"].apply(lambda x: x["country"])
        self._data = self._data[["lat", "lon", "country"]]
        self._data = self._data.to_dict(orient="records")



def get_boundingbox_country(country, output_as='boundingbox'):
    output = None
    url = 'http://nominatim.openstreetmap.org/search?country={country}&format=json&polygon=0'

    response = [grequests.get(url.format(country=country))]
    results = grequests.map(response)
    results = list(itertools.chain.from_iterable([
        query.json()
        for query in results
    ]))

    if len(results) == 1:

        if output_as == 'boundingbox':
            print("aaaaaaaaaa", results)
            output = results[0][output_as]

        if output_as == 'center':
            output = [results[0]['lat'], results[0]['lon']]

        output = list(map(lambda x: float(x), output))

    return output

