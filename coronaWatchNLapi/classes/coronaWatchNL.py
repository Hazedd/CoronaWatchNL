import copy
import csv
import datetime
import io
import requests
import geojson

from coronaWatchNLapi.helpers.dateTimeEncoder import DateTimeEncoder


class CoronaWatchNL(object):
    """

    """
    def __init__(self):
        """
        Base to parse and process data
        """
        # privates
        self._url_csv_corona_data_gemeenten = "https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_corona_in_nl_table.csv"
        # self._url_csv_gemeenten_geojson = "https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/ext/gemeente-2019.geojson"
        self._url_csv_gemeenten_geojson = "https://cartomap.github.io/nl/wgs84/gemeente_2019.geojson"
        self._url_csv_gemeenten_stats = "https://raw.githubusercontent.com/Hazedd/CoronaWatchNL/master/ext/Gemeenten_kerncijfers_2019.csv"
        self._url_csv_opp = "https://raw.githubusercontent.com/Hazedd/CoronaWatchNL/master/ext/gemeente_opp.csv"
        # pubs
        self.corona_data_dict = {}
        self.gemeenten_geojson = {}
        self.gemeenten_stats = {}
        self.gemeenten_opp = {}
        # construct
        self._construct()

    def _construct(self):
        """
        Private method to parse and combine data
        :return:
        """
        # download and parse
        csv_dict_reader = self._download_data_as_csv_dict_reader(self._url_csv_corona_data_gemeenten)
        self.corona_data_dict = self._prep_corona_data(csv_dict_reader)

        csv_dict_reader = self._download_data_as_csv_dict_reader(self._url_csv_gemeenten_stats, ";")
        self.gemeenten_stats = self._prep_gemeenten_kerncijfer(csv_dict_reader)

        downloaded_geojson = self._download_geojson()
        self.gemeenten_geojson = self._prep_geojson(downloaded_geojson)

        csv_dict_reader = self._download_data_as_csv_dict_reader(self._url_csv_opp, ";")
        self.gemeenten_opp = self._prep_gemeenten_opp(csv_dict_reader)

    def _download_data_as_csv_dict_reader(self, url, delimiter_value=","):
        """
        Private method to download a csv and returns a csv dict reader object
        :param url: url of csv
        :param delimiter_value: delimiter value (default ",")
        :return: csv.DictReader object
        """
        with requests.Session() as session:
            downloaded_data = session.get(url)
            dict_object = csv.DictReader(io.StringIO(downloaded_data.text), delimiter=delimiter_value)
        return dict_object

    def _download_geojson(self):
        """
        Private method to download geojson and returns geojson feature collection
        :return: geojson feature collection
        """
        with requests.Session() as session:
            download = session.get(self._url_csv_gemeenten_geojson)
        dump = geojson.dumps(download.json(), sort_keys=True)
        return geojson.loads(dump)

    def _prep_geojson(self, geojson_data):
        """
        Private method that preps the feature collection.
          - Adds gemeente name en provincie name data.
          - removes ArcGIS pro unsupported field (shape lengte)
          - removes Gemeenten_ as it is a duplicated id
        :param geojson_data: geojson feature collection
        :return: cleaned geojson feature collection
        """
        for item in geojson_data.features:
            key = str(int(str(item.properties['statcode']).replace("GM", "")))
            item.properties['Gemnr'] = int(key)
            item.properties['Gemeentenaam'] = self.corona_data_dict[key]['Gemeentenaam']
            item.properties['Provincienaam'] = self.corona_data_dict[key]['Provincienaam']
            for key in ["FID", "jrstatcode", "statnaam"]:
                del item.properties[f"{key}"]
        return geojson_data

    @staticmethod
    def _prep_gemeenten_kerncijfer(csv_dict_reader):
        import pprint as pp
        """
        Private method that creates a gemeenten kerncijfer dict. Key is a stripped gemeente id
        :param csv_dict_reader:
        :return: dict of gemeenten kerncijfers, key is gemeente id.
        """
        out_dict = {}
        for row in csv_dict_reader:
            out_dict[f"{int(row['gwb_code_8'])}"] = row
        return out_dict

    @staticmethod
    def _prep_gemeenten_opp(csv_dict_reader):
        """
        Private method that creates a gemeenten kerncijfer dict. Key is a stripped gemeente id
        :param csv_dict_reader:
        :return: dict of gemeenten kerncijfers, key is gemeente id.
        """
        out_dict = {}
        for row in csv_dict_reader:
            out_dict[f"{int(row['gem_code'])}"] = row
        return out_dict


    @staticmethod
    def _prep_corona_data(csv_dict_reader):
        """
        Private method that creates a corona data dict. Key is a stripped gemeente id.
          Time series as a dict {total_count, new, datetime object}
        :param csv_dict_reader: csv.DictReader object
        :return: dict of corona data, key is gemeente id.
        """
        list_of_dicts = []
        for row in csv_dict_reader:
            new_dict = {"Gemeentenaam": row["Gemeentenaam"],
                        "Provincienaam": row["Provincienaam"],
                        "Gemeentecode": row["Gemeentecode"]}
            # remove items
            for item in ["Gemeentenaam", "Provincienaam", "Gemeentecode"]:
                del row[f"{item}"]
            # create dict and append to list
            new_dict["timeseries"] = dict(row)
            list_of_dicts.append(new_dict)
        # make dict out of list
        out_dict = {}
        for item in list_of_dicts:
            list_of_dicts = []
            last_value = 0
            # make count on time series
            for k, v in item["timeseries"].items():
                data_dict = {"total_count": int(v),
                             "new": int(v) - last_value,
                             "date": datetime.datetime.strptime(k, '%Y-%m-%d')}
                list_of_dicts.append(data_dict)
                last_value = int(v)
            item["total_count"] = int(v)
            item["timeseries"] = list_of_dicts
            # strore in dict of dicts
            out_dict[item["Gemeentecode"]] = item
        return out_dict

    @staticmethod
    def _get_geojson_feature_with_stats(gem_id, stat_dict, gemeenten_geojson):
        """
        Private method to adds stats on geojson, matching on gemeente key.
        :param gem_id: gemeente key
        :param stat_dict: dict of keys and values
        :param gemeenten_geojson: geojson feature collection
        :return: geojson feature collection including keys and values from stat_dict
        """
        # todo: remove loop, makes it slow as fuk
        for item in gemeenten_geojson.features:
            if item.properties['Gemnr'] == int(gem_id):
                for key, value in stat_dict.items():
                    item.properties[key] = value
                return item

    def get_geojson_from_dataset(self, dataset):
        """
        ...
        :param dataset:
        :return:
        """
        gemeenten_geojson = copy.deepcopy(self.gemeenten_geojson)
        output_feature_list = []
        for key, value in dataset.items():
            feature = self._get_geojson_feature_with_stats(key, value, gemeenten_geojson)
            # feature.properties["dataset_name"] = dataset["name"]
            output_feature_list.append(feature)

        geojson_output = dict(geojson.FeatureCollection(output_feature_list))
        # geojson_output["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::28992"}}
        return geojson_output


    def _get_geojson_from_data(self, data, indent=2):
        return geojson.dumps(data, sort_keys=True, cls=DateTimeEncoder, indent=indent)

    def _save_geojson_to_file(self, dump, file_path):
        with open(file_path, "w") as f:
            f.write(dump)

    def save_dataset_as_geojson(self, dataset, file_path):
        geojson_dump = self._get_geojson_from_data(dataset)
        self._save_geojson_to_file(geojson_dump, file_path)
