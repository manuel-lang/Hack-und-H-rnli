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

### User Specifics
#######################################################

# Specify if you want to train a new model or use a trained Model
train_new_model = True

### Import Data
######################################################

df = pd.read_csv("data/input_data.csv")

# Rename columns
header=df.columns
df.rename(columns={header[0]: "time",
           header[1]: "wind actual",
           header[2]: "price forecast",
           header[3]: "price actual"}, inplace=True)
df.reset_index()
df.set_index("time")
df["time"] = pd.to_datetime(df["time"], utc=True)

# Transform DataFrame to Time Series Object
df_series = TimeSeries.from_dataframe(df[["time","price actual"]], time_col='time', value_cols="price actual")

### Train and Test Model
#######################################################

# Train Test Split
train, val = df_series.split_before(pd.Timestamp("2021-03-01 00:00:00+00:00"))

# Normalize the time series (note: we avoid fitting the transformer on the validation set)
transformer = Scaler()
train_transformed = transformer.fit_transform(train)
val_transformed = transformer.transform(val)
series_transformed = transformer.transform(df_series)

# Define the LSTM Model parameters
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

# Either train a new model or load best model from checkpoint
if train_new_model==True:
    my_model.fit(train_transformed, val_series=val_transformed, verbose=True)
else:
    my_model = RNNModel.load_from_checkpoint(model_name='Forecast_LSTM_next_hour', best=True)

# Evaluate Predictions 
def eval_model(model):
    pred_series = model.predict(n=len(val_transformed))

    plt.figure(figsize=(8,5))
    val_transformed.plot(label='actual')
    pred_series.plot(label='forecast')
    plt.title('MAPE: {:.2f}%'.format(mape(pred_series, val_transformed)))
    plt.legend()
    plt.show()

def backtest(model):
    backtest_series = model.historical_forecasts(series_transformed,
                                start=pd.Timestamp("2021-03-01 00:00:00+00:00"),
                                forecast_horizon=1,
                                retrain=False,
                                verbose=True)

    plt.figure(figsize=(8,5))
    slice_series_transformed = series_transformed.slice(pd.Timestamp("2021-03-01 00:00:00+00:00"), pd.Timestamp("2021-03-19 23:00:00+01:00"))
    transformer.inverse_transform(slice_series_transformed).plot(label='actual')
    transformer.inverse_transform(backtest_series).plot(label='backtest')
    plt.legend()
    plt.title('Backtest, starting March 2021')
    plt.show();

backtest(my_model)