
from shake_me_backend.core.data_helper import ImportUsgsEarthquakeData



def test_get_data(start_date, end_date, min_lat , max_lat , min_lng , max_lng):
    data = ImportUsgsEarthquakeData(start_date, end_date, min_lat , max_lat , min_lng , max_lng)

    map_data = data.map_jsondata()
    chart_data = data.chart_jsondata()

    assert len(map_data) == 277
    assert len(chart_data) == 7