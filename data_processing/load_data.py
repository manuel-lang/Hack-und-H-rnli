import wapi
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd

client_id = "kU4j3zAKMPOKK4dCVYh2t_tSjRKf2mYY"
client_secret = "ElZ9zXapi2quS6_.ciyRaBktTflNGLiU04EH5qM1Pm1zvMKpFoxTS4lnhL_ZfAl7KeDwx5fRENTJ9G58K2zWgcmItmSW_-kcQHPE"

def load_data() -> pd.DataFrame:
    session = wapi.Session(client_id=client_id, client_secret=client_secret)

    start_date = "2019-01-01"
    date_today = datetime.today().strftime('%Y-%m-%d')

    historic_wind_curve_name = "pro de-amp wnd da tso mwh/h cet min15 f"
    price_forecasts_curve_name = "pri de spot €/mwh cet min15 a"
    historic_prizes_curve_name = "vol de imb sys mw cet min15 a"

    curve_names = [historic_wind_curve_name, price_forecasts_curve_name, historic_prizes_curve_name]

    df = pd.DataFrame()
    for curve_name in curve_names:
        curve = session.get_curve(name=curve_name)
        data = curve.get_data(data_from=start_date, data_to=date_today)
        pd_data = data.to_pandas()
        df[curve_name] = pd_data

    return df.resample('60min').mean()

if __name__ == "__main__":
    df = load_data()
    df.to_csv("data/input_data.csv")
    print(df.index[0:3])
