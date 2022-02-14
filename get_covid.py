import pandas as pd
import datetime
import os
import git

def data_update():
    g = git.cmd.Git(".\data\COVID-19")
    g.pull()

def get_new_confirmed(dt: str, country: str):
    # dt in YYYY-MM-DD
    if dt:
        dt = [int(num) for num in dt.split("-")]
        dt = datetime.date(dt[0], dt[1], dt[2])
    else:
        dt = datetime.datetime.today() if not dt else dt

    path_src = "./data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
    files = [file.split('.')[0] for file in os.listdir(path_src)]

    dt_1 = dt
    dt_1_str = dt_1.strftime("%m-%d-%Y")
    for retry in range(5):
        dt_1 = dt_1 - datetime.timedelta(days=1)
        dt_1_str = dt_1.strftime("%m-%d-%Y")
        if dt_1_str in files:
            break
        elif retry > 1:
            data_update()
        elif retry == 5:
            return f"now data found in the last {retry} days"

    dt_2 = dt_1 - datetime.timedelta(days=1)
    dt_2_str = dt_2.strftime("%m-%d-%Y")

    df_1 = pd.read_csv(path_src + "/" + f"{dt_1_str}.csv")
    df_2 = pd.read_csv(path_src + "/" + f"{dt_2_str}.csv")
    if country not in df_1['Country_Region'].values:
        return "country error"
    confirmed_1 = sum(df_1['Confirmed'].loc[df_1['Country_Region'] == country])
    confirmed_2 = sum(df_2['Confirmed'].loc[df_2['Country_Region'] == country])
    diff = confirmed_1 - confirmed_2

    dt_1_str_YMD = dt_1.strftime("%Y-%m-%d")
    dt_2_str_YMD = dt_2.strftime("%Y-%m-%d")

    res = f"New confirmed\n{country}\nfrom {dt_2_str_YMD} to {dt_1_str_YMD} is {diff}\nBRAVO!"
    return res

if __name__ == "__main__":
    test = pd.read_csv("./test.csv")
    get_new_confirmed(country="Italy", dt="")
