from flask import Flask, jsonify, make_response
from flask_restplus import Resource, Api
import folium
import pandas as pd


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
        return cWatchNL.actual()


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


@nsCoronaWatch.route('/getHistorical')
class GetHistorical(Resource):
    def get(self):
        return cWatchNL.get_historical()


@nsCoronaWatch.route('/getHistoricalGeojson')
class GetHistoricalGeojson(Resource):
    def get(self):
        dataset = cWatchNL.get_historical()
        return jsonify(cWatchNL.get_geojson_from_dataset(dataset))


@nsCoronaWatch.route('/map')
class GetMap(Resource):
    def get(self):
        def get_map(dataset, value, layer_name, legend_name="unknown"):
            data = pd.DataFrame.from_dict(dataset, orient='index')
            # check if values are below 0
            if data[f"{value}"].min() <= 0:
                color = "OrRd"  # "BuPu"
            else:
                color = "OrRd"  # "PuBuGn"

            bins = [0, 1, 2, 3, 4, 6, 12]

            return folium.Choropleth(
                geo_data=cWatchNL.gemeenten_geojson,
                name=f'{layer_name}',
                data=data,
                columns=['gemNr', f'{value}'],
                key_on='feature.id',
                fill_color=f'{color}',
                fill_opacity=0.5,
                line_opacity=0.81,
                line_color="#ededed",
                legend_name=f'{legend_name}',
                nan_fill_opacity=0,
                highlight=True,
            )

        start_coords = (52.0978432,5.1150848)
        m = folium.Map(location=start_coords, zoom_start=7,
                       width='50%', height='100%')
                       # tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
                       # attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
                       # )

        get_map(cWatchNL.actual(), 'total_count', "total count", "meest recente totaal aantal besmettingen").add_to(m)
        get_map(cWatchNL.actual(), 'new', "new", "meest recente officiele nieuwe besmettingen").add_to(m)
        get_map(cWatchNL.increase_of_last_days(), 'mean', "growth mean", "gemiddelde groei over 7 dagen").add_to(m)
        folium.LayerControl().add_to(m)


        return make_response(m._repr_html_())


if __name__ == '__main__':
    app.run(debug=True)
