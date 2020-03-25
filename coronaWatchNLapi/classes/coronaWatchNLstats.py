import statistics

from coronaWatchNLapi.classes.coronaWatchNL import CoronaWatchNL

class CoronaWatchStatsNL(CoronaWatchNL):
    def __init__(self):
        super().__init__()


    def actual(self):
        out_dict = {}
        # out_dict["name"] = "def gown_rate"
        for key, value in self.corona_data_dict.items():
            timeseries = value["timeseries"]
            object_dict = {}
            object_dict["Gemeentenaam"] = value['Gemeentenaam']
            object_dict["gemNr"] = f"GM{int(key):04d}"
            object_dict["total_count"] = timeseries[-1]["total_count"]
            object_dict["new"] = timeseries[-1]["new"]

            try:
                object_dict["growth"] = (timeseries[-1]["total_count"] - timeseries[-2]["total_count"]) \
                                        / timeseries[-1]["total_count"] * 100
            except:
                object_dict["growth"] = None

            out_dict[key] = object_dict
        return out_dict


    def increase_of_last_days(self, days=14):
        out_dict = {}
        for key, item in self.corona_data_dict.items():
            timeseries = item["timeseries"]
            object_dict = {}
            object_dict["gemNr"] = f"GM{int(key):04d}"
            out_list = []
            for idx in range(2, (days+1)):
                try:
                    value = (timeseries[-idx + 1]["total_count"] - timeseries[-idx]["total_count"]) \
                            / timeseries[-idx + 1]["total_count"] * 100
                    out_list.append(value)
                    object_dict[f"{timeseries[-idx]['date'].strftime('%m/%d/%Y')}-{timeseries[-idx+1]['date'].strftime('%m/%d/%Y')}"] = value

                except:
                    object_dict[f"{timeseries[-idx]['date'].strftime('%m/%d/%Y')}"] = None

            try:
                object_dict["mean"] = statistics.mean(out_list)
            except:
                object_dict["mean"] = None

            # for item2 in timeseries:
            #     object_dict[f"date_{item2['date'].strftime('%m/%d/%Y')}"] = item2['total_count']

            out_dict[key] = object_dict
        return out_dict

    def growth_rate(self):
        out_dict = {}
        for key, value in self.corona_data_dict.items():
            timeseries = value["timeseries"]
            object_dict = {}
            object_dict["total_count"] = value["total_count"]
            for item in timeseries:
                object_dict[f"date_{item['date'].strftime('%m/%d/%Y')}"] = item['total_count']

            for idx in [3, 7, 14]:
                try:
                    stat_value = ((timeseries[-1]["total_count"] / timeseries[-(idx)]["total_count"])**(1/(idx-1))-1)*100
                except:
                    stat_value = None
                object_dict[f"growth_rate_last_{idx}_days"] = stat_value

            out_dict[key] = object_dict
        return out_dict


    def get_historical(self):
        out_dict = {}
        for key, value in self.corona_data_dict.items():
            timeseries = value["timeseries"]
            object_dict = {}
            object_dict["total_count"] = value["total_count"]
            for item in timeseries:
                object_dict[f"date_{item['date'].strftime('%m/%d/%Y')}"] = item['total_count']
            out_dict[key] = object_dict
        return out_dict

