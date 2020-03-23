from coronaWatchNLapi.classes.CoronaWatchStatsNL import CoronaWatchStatsNL

cWatchNL = CoronaWatchStatsNL()
cWatchNL_dataset = cWatchNL.actual()
geojson_thing = cWatchNL.get_geojson_from_dataset(cWatchNL_dataset)


class tester():
    # todo: make proper inner outer for saving geojson
    cWatchNL.save_dataset_as_geojson(geojson_thing, r"files\totaal.geojson")

    cWatchNL_dataset = cWatchNL.increase_of_last_days()
    geojson_thing = cWatchNL.get_geojson_from_dataset(cWatchNL_dataset)

    # todo: make proper inner outer for saving geojson
    cWatchNL.save_dataset_as_geojson(geojson_thing, r"files\increase_of_last_days.geojson")

    cWatchNL_dataset = cWatchNL.growth_rate()
    geojson_thing = cWatchNL.get_geojson_from_dataset(cWatchNL_dataset)

    # todo: make proper inner outer for saving geojson
    cWatchNL.save_dataset_as_geojson(geojson_thing, r"files\growth_rate.geojson")