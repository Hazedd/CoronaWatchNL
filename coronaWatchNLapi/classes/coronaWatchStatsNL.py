import statistics

from coronaWatchNLapi.classes.coronaWatchNL import CoronaWatchNL

class CoronaWatchStatsNL(CoronaWatchNL):
    def __init__(self):
        super().__init__()

    def increase_of_last_days(self, days=7):
        out_dict = {}
        # out_dict["name"] = "increase_of_last_days"
        for key, item in self.corona_data_dict.items():
            timeseries = item["timeseries"]
            object_dict = {}
            out_list = []
            for idx in range(2, (days+1)):
                ###################################################
                try:
                    # for every day, calculate % of increase
                    value = (timeseries[-idx + 1]["total_count"] - timeseries[-idx]["total_count"]) / timeseries[-idx + 1]["total_count"] * 100
                    out_list.append(value)
                    object_dict[f"x-{idx - 1}"] = value
                except:
                    object_dict[f"x-{idx - 1}"] = None
            try:
                object_dict["mean"] = statistics.mean(out_list)
            except:
                object_dict["mean"] = None
            ###################################################
            out_dict[key] = object_dict
        return out_dict

    def actual(self):
        out_dict = {}
        # out_dict["name"] = "def gown_rate"
        for key, value in self.corona_data_dict.items():
            timeseries = value["timeseries"]
            object_dict = {}
            object_dict["total_count"] = timeseries[-1]["total_count"]
            object_dict["new"] = timeseries[-1]["new"]
            try:
                object_dict["growth"] = (timeseries[-1]["total_count"] - timeseries[-2]["total_count"]) / timeseries[-1]["total_count"] * 100
            except:
                object_dict["growth"] = None

            for item in timeseries:
                object_dict[f"date_{item['date'].strftime('%m/%d/%Y')}"] = item['total_count']

            out_dict[key] = object_dict
        return out_dict

    def growth_rate(self):
        out_dict = {}
        # out_dict["name"] = "def gown_rate"
        for key, value in self.corona_data_dict.items():
            timeseries = value["timeseries"]
            object_dict = {}
            ###################################################
            for item in timeseries:
                object_dict[f"date_{item['date'].strftime('%m/%d/%Y')}"] = item['total_count']
            ###################################################
            for idx in [3, 7, 14]:
                try:
                    stat_value = ((timeseries[-1]["total_count"] / timeseries[-(idx)]["total_count"]) ** (1 / (idx-1)) - 1 ) * 100
                except:
                    stat_value = None
                object_dict[f"growth_rate_last_{idx}_days"] = stat_value
            ###################################################
            out_dict[key] = object_dict
        return out_dict