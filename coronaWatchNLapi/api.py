from flask import Flask, jsonify
from flask_restplus import Resource, Api

from coronaWatchNLapi.classes.coronaWatchNLstats import CoronaWatchStatsNL
cWatchNL = CoronaWatchStatsNL()

app = Flask(__name__)
api = Api(app, version='0.0.1', title='CoronaWatchNL API',
          description='CoronaWatchNLApi',
          )

nsCoronaWatch = api.namespace('coronaWatchNL', description='CoronaWatchNL data and stats')


@nsCoronaWatch.route('/getActual')
class GetActual(Resource):
    def get(self):
        dataset = cWatchNL.actual()
        return jsonify(cWatchNL.get_geojson_from_dataset(dataset))


@nsCoronaWatch.route('/getActualGeojson')
class GetActualGeojson(Resource):
    def get(self):
        dataset = cWatchNL.actual()
        return jsonify(cWatchNL.get_geojson_from_dataset(dataset))


@nsCoronaWatch.route('/getIncreaseOfLastDays')
class GetIncreaseOfLastDays(Resource):
    def get(self):
        return cWatchNL.increase_of_last_days()


@nsCoronaWatch.route('/getIncreaseOfLastDaysGeojson')
class GetIncreaseOfLastDaysGeojson(Resource):
    def get(self):
        dataset = cWatchNL.increase_of_last_days()
        return jsonify(cWatchNL.get_geojson_from_dataset(dataset))


@nsCoronaWatch.route('/getGrowthRate')
class GetGrowthRate(Resource):
    def get(self):
        return cWatchNL.growth_rate()


@nsCoronaWatch.route('/getGrowthRateGeojson')
class GetIncreaseOfLastDays(Resource):
    def get(self):
        dataset = cWatchNL.growth_rate()
        return jsonify(cWatchNL.get_geojson_from_dataset(dataset))


if __name__ == '__main__':
    app.run(debug=True)
