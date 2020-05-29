
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
from flask_cors import CORS

from shake_me_backend.core.data_helper import ImportUsgsEarthquakeData



def app():

    url_prefix = '/api/v1'
    geom_api = Blueprint(
        'earthquake_api',
        __name__,
        template_folder='templates',
        url_prefix=url_prefix
    )

    def bad_request(message, error_value):
        response = jsonify({'message': message})
        response.status_code = error_value
        return response

    @geom_api.route('/mapdata', methods=['GET'])
    def get_grid():

        url_arg_keys = {
            "start_date": request.args.get('start_date', type=str, default="2000-01-01"),
            "end_date": request.args.get('end_date', type=str, default="2001-01-01"),
            "min_lat": request.args.get('min_lat', type=float),
            "min_lng": request.args.get('min_lng', type=float),
            "max_lat": request.args.get('max_lat', type=float),
            "max_lng": request.args.get('max_lng', type=float),
        }


        try:
            data = ImportUsgsEarthquakeData(
                start_date=url_arg_keys["start_date"],
                end_date=url_arg_keys["end_date"],
                min_lat=url_arg_keys["min_lat"],
                max_lat=url_arg_keys["max_lat"],
                min_lng=url_arg_keys["min_lng"],
                max_lng=url_arg_keys["max_lng"]
            )

            output = jsonify(
                {
                    "map_data": data.map_jsondata(),
                    "chart_data": data.chart_jsondata()
                }
            )

            output.headers.add('Access-Control-Allow-Origin', '*')

            return output

        except (ValueError) as err:
            err = repr(err)
            return bad_request(err, 400)

    app = Flask(__name__)
    CORS(app)

    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.register_blueprint(geom_api)

    return app


app = app()

if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()
    app.run(port=5000, debug=True)


