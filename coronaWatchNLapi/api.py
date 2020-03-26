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


def style_function_new(feature):
    color = "Red"
    value = feature.properties["new"]
    if value == 0 or value is None:
        color = "Black"
    elif feature.properties["new"] <= 5:
        color = 'green'
    elif feature.properties["new"] <= 25:
        color = 'orange'

    return {
        'fillOpacity': 0.5,
        'weight': 0.5,
        'fillColor': f'{color}'
    }


def style_function_total_count(feature):
    color = "Red"
    value = feature.properties["total_count"]
    if value == 0 or value is None:
        color = "Black"
    elif feature.properties["total_count"] <= 25:
        color = 'green'
    elif feature.properties["total_count"] <= 50:
        color = 'orange'

    return {
        'fillOpacity': 0.5,
        'weight': 0.5,
        'fillColor': f'{color}'
    }


def style_function_growth(feature):
    color = "Red"
    value = feature.properties["mean"]
    if value == 0 or value is None:
        color = "Black"
    elif feature.properties["mean"] <= 25:
        color = 'green'
    elif feature.properties["mean"] <= 50:
        color = 'orange'

    return {
        'fillOpacity': 0.5,
        'weight': 0.5,
        'fillColor': f'{color}',
        'popup': "tester"
    }


@nsCoronaWatch.route('/map')
class GetMap(Resource):
    def get(self):
        def get_map(dataset, value, layer_name, show=True):

            if value == "new":
                style_function = style_function_new
            elif value == "total_count":
                style_function = style_function_total_count
            elif value == "mean":
                style_function = style_function_growth

            return folium.GeoJson(cWatchNL.get_geojson_from_dataset(dataset),
                                  show=show,
                                  name=f'{layer_name}',
                                  style_function=style_function,
                                  tooltip=folium.features.GeoJsonTooltip(
                                      fields=['Gemeentenaam', f'{value}'],
                                      localize=True),
                                  # popup=folium.GeoJsonPopup(
                                  #     ['Gemeentenaam', f'{value}'],
                                  #     localize=True)
                                  )

        start_coords = (52.0978432, 5.1150848)
        m = folium.Map(location=start_coords, zoom_start=8,
                       width='50%', height='100%',
                       tiles=None,
                       name="tester")

        folium.TileLayer(tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
                         attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
                         name='basemap dark',
                         overlay=False, control=False).add_to(m)

        get_map(cWatchNL.actual(), 'total_count', "totaal aantal besmettingen",  True).add_to(m)
        get_map(cWatchNL.actual(), 'new', "aantal nieuwe besmettingen", False).add_to(m)
        get_map(cWatchNL.increase_of_last_days(), 'mean', "gemiddelde groei over 3 dagen", False).add_to(m)

        folium.LayerControl(collapsed=True).add_to(m)

        return make_response(m._repr_html_())


if __name__ == '__main__':
    app.run(debug=True)



#
# layer_geom = folium.FeatureGroup(name='layer',control=False)
#
# for i in range(len(data_geojson_dict["features"])):
#     temp_geojson = {"features":[data_geojson_dict["features"][i]],"type":"FeatureCollection"}
#     temp_geojson_layer = folium.GeoJson(temp_geojson,
#                    highlight_function=lambda x: {'weight':3, 'color':'black'},
#                     control=False,
#                     style_function=lambda feature: {
#                    'color': 'black',
#                    'weight': 1},
#                     tooltip=folium.features.GeoJsonTooltip(fields=list_tooltip_vars,
#                                         aliases=[x.capitalize()+":" for x in list_tooltip_vars],
#                                           labels=True,
#                                           sticky=False))
#     folium.Popup(temp_geojson["features"][0]["properties"]["productor"]).add_to(temp_geojson_layer)
#     temp_geojson_layer.add_to(layer_geom)
#
# layer_geom.add_to(m)
# folium.LayerControl(autoZIndex=False, collapsed=True).add_to(m)
