"""
Date: 20.03.2021
Team: Hack & Hörnli

Time Series Forecasting Model based on Unit8 Darts

"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns

from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import (
    NaiveSeasonal,
    NaiveDrift,
    Prophet,
    ExponentialSmoothing,
    ARIMA,
    AutoARIMA,
    StandardRegressionModel,
    Theta,
    FFT,
    RNNModel
)
from darts.metrics import mape, mase
from darts.utils.statistics import check_seasonality, plot_acf, plot_residuals_analysis

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import shutil
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm_notebook as tqdm

from torch.utils.tensorboard import SummaryWriter

import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)

import os
import wapi

# Doesn't work for some odd reason
# sys.path.insert(0, './data_processing/load_data')
# from data_processing.load_data import load_data


### Import Data
######################################################

df = pd.read_csv("data/input_data.csv")
header=df.columns
df.rename(columns={header[0]: "time",
           header[1]: "wind actual",
           header[2]: "price forecast",
           header[3]: "price actual"}, inplace=True)
df.reset_index()
df.set_index("time")
df["time"] = pd.to_datetime(df["time"], utc=True)

df_series = TimeSeries.from_dataframe(df[["time","price actual"]], time_col='time', value_cols="price actual")

# sns.set_theme()

# plt.figure(figsize=(10,5))
# plt.suptitle("Time Series", fontsize=20)
# plt.plot(df.iloc[:1000,2],label='predicted price')
# plt.plot(df.iloc[:1000,3],label='actual price')
# # plt.xticks(np.arange(100))
# plt.legend()
# plt.show()

# plt.figure(figsize=(10,5))
# plt.suptitle("Time Series", fontsize=20)
# plt.plot(df.iloc[:1000,1],label='wind actual')
# # plt.xticks(np.arange(100))
# plt.legend()
# plt.show()

### Train and Test Model
#######################################################

train, val = df_series.split_before(pd.Timestamp("2021-03-01 00:00:00+00:00"))

# Normalize the time series (note: we avoid fitting the transformer on the validation set)
transformer = Scaler()
train_transformed = transformer.fit_transform(train)
val_transformed = transformer.transform(val)
series_transformed = transformer.transform(df_series)

my_model = RNNModel(
    model='LSTM',
    input_chunk_length=24,
    output_chunk_length=1,
    hidden_size=25,
    n_rnn_layers=1,
    dropout=0.2,
    batch_size=16,
    n_epochs=20,
    optimizer_kwargs={'lr': 1e-3},
    model_name='Forecast_LSTM_next_hour',
    log_tensorboard=True,
    random_state=42
)

# my_model.fit(train_transformed, val_series=val_transformed, verbose=True)
my_model = RNNModel.load_from_checkpoint(model_name='Forecast_LSTM_next_hour', best=True)

def eval_model(model):
    pred_series = model.predict(n=len(val_transformed))

    plt.figure(figsize=(8,5))
    val_transformed.plot(label='actual')
    pred_series.plot(label='forecast')
    plt.title('MAPE: {:.2f}%'.format(mape(pred_series, val_transformed)))
    plt.legend()
    plt.show()

# eval_model(my_model)
def backtest(model):
    backtest_series = model.historical_forecasts(series_transformed,
                                start=pd.Timestamp("2021-03-01 00:00:00+00:00"),
                                forecast_horizon=1,
                                retrain=False,
                                verbose=True)


    plt.figure(figsize=(8,5))
    slice_series_transformed = series_transformed.slice(pd.Timestamp("2021-03-01 00:00:00+00:00"), pd.Timestamp("2021-03-19 23:00:00+01:00"))
    slice_series_transformed.plot(label='actual')
    backtest_series.plot(label='backtest')
    plt.legend()
    plt.title('Backtest, starting March 2021')
    plt.show();

    plt.figure(figsize=(8,5))
    slice_series_transformed = series_transformed.slice(pd.Timestamp("2021-03-01 00:00:00+00:00"), pd.Timestamp("2021-03-19 23:00:00+01:00"))
    transformer.inverse_transform(slice_series_transformed).plot(label='actual')
    transformer.inverse_transform(backtest_series).plot(label='backtest')
    plt.legend()
    plt.title('Backtest, starting March 2021')
    plt.show();

    df_output = transformer.inverse_transform(backtest_series).pd_dataframe()
    cols = df_output.columns
    df_output.rename({cols[0]: 'Forecast'}, inplace=True)
    df_output.to_csv("data/forecast.csv")

    df_output_2 = transformer.inverse_transform(slice_series_transformed).pd_dataframe()
    cols = df_output_2.columns
    df_output_2.rename({cols[0]: 'Actual Price'}, inplace=True)
    df_output_2.to_csv("data/actual_price.csv")

    print(df_output.shape)
    print(df_output.columns)
    # df_output["Price Actual"] = slice_series_transformed.slice(pd.Timestamp("2021-03-01 00:00:00+00:00"), pd.Timestamp("2021-03-19 21:00:00+00:00"))
    # df_output.rename({"0":"Forecast"}, inplace=True)
    # print('MAPE: {:.2f}%'.format(mape(transformer.inverse_transform(series_transformed),
    #                                 transformer.inverse_transform(backtest_series))))

backtest(my_model)