from numpy import datetime_as_string
import pandas as pd
import datetime
import os
# import git
import yaml

with open('./configs/covid.yaml', "r") as f:
    CONFIG = yaml.safe_load(f)

def make_rabbit(smth):
    rabbit = f" (\_/)\n(・_・)\n/  >{smth}\n"
    return rabbit

def kw_to_country(kw: str):
    k2c = CONFIG['k2c']
    if kw.lower() in k2c:
        return k2c[kw.lower()]
    else:
        return kw.title()

def get_new_confirmed(country: str, dt: int=20)->str:

    def bar_chat(data: list[datetime.datetime, int]):
        max_val = max(data, key=lambda x:x[1])[1]
        tmp = [[item[0].strftime("%Y-%m-%d"), round(item[1]/max_val*20)] for item in data]
        res = f"```{country} new cases {dt}-days trend\n"
        for item in tmp:
            res += item[0] + "  " + '█'*item[1] + "\n"
        res += f"In {tmp[-1][0]}, the new confirmed cases:\n"
        res += make_rabbit(data[-1][-1])
        res += "```"
        return res
    # data_update()
    # dt in YYYY-MM-DD
    print(CONFIG)
    country = kw_to_country(kw=country)
    print(country)
    # path_src = "./data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
    path_src = CONFIG['path_src']
    files = [file.split('.')[0] for file in os.listdir(path_src)]

    t_1 = datetime.datetime.now()
    t_1_mdy = t_1.strftime("%m-%d-%Y")

    for retry in range(5):
        t_1 = t_1 - datetime.timedelta(days=1)
        t_1_mdy = t_1.strftime("%m-%d-%Y")
        if t_1_mdy in files:
            break
        elif retry == 5:
            return f"now data found in the last {retry} days"

    ts = [t_1-datetime.timedelta(days=i) for i in range(0, dt+1)]
    info = list()
    for t in ts:
        t_mdy = t.strftime("%m-%d-%Y")
        tmp = pd.read_csv(path_src + "/" + f"{t_mdy}.csv")
        if country not in tmp['Country_Region'].values:
            return "country error"
        info.append([t, sum(tmp['Confirmed'].loc[tmp['Country_Region'] == country])])
    
    for i in range(len(info)-1):
        info[i][-1] =  info[i][-1]  - info[i+1][-1]
    info.pop()
    info = info[::-1]
    # dt_2 = t_1 - datetime.timedelta(days=1)
    # dt_2_mdy = dt_2.strftime("%m-%d-%Y")

    # df_1 = pd.read_csv(path_src + "/" + f"{t_1_mdy}.csv")
    # df_2 = pd.read_csv(path_src + "/" + f"{dt_2_mdy}.csv")
    # if country not in df_1['Country_Region'].values:
    #     return "country error"
    # confirmed_1 = sum(df_1['Confirmed'].loc[df_1['Country_Region'] == country])
    # # confirmed_2 = sum(df_2['Confirmed'].loc[df_2['Country_Region'] == country])
    # diff = confirmed_1 - confirmed_2

    # dt_1_str_ymd = t_1.strftime("%Y-%m-%d")
    # dt_2_str_ymd = dt_2.strftime("%Y-%m-%d")

    # res = f"New confirmed\n{country}\nfrom {dt_2_str_ymd} to {dt_1_str_ymd} is {diff}\nBRAVO!"
    res = bar_chat(info)
    return res

if __name__ == "__main__":
    data = pd.read_csv('/home/si9h/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv')
    res = get_new_confirmed(country="Germany", dt=20)
