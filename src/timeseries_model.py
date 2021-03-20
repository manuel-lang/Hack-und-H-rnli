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
#######################################################
# df = pd.read_csv('https://raw.githubusercontent.com/unit8co/darts/master/examples/AirPassengers.csv')
# series = TimeSeries.from_dataframe(df, 'Month', '#Passengers')

df = pd.read_csv("data/input_data.csv")
print(df.shape)
print(df.columns)

# print(df.iloc[:,0])
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

print(np.sum(df.iloc[:,1]-df.iloc[:,3]))
'''
### Train and Test Model
#######################################################

train, val = series.split_before(pd.Timestamp('19580101'))

# Normalize the time series (note: we avoid fitting the transformer on the validation set)
transformer = Scaler()
train_transformed = transformer.fit_transform(train)
val_transformed = transformer.transform(val)
series_transformed = transformer.transform(series)

my_model = RNNModel(
    model='LSTM',
    input_chunk_length=12,
    output_chunk_length=1,
    hidden_size=25,
    n_rnn_layers=1,
    dropout=0.4,
    batch_size=16,
    n_epochs=400,
    optimizer_kwargs={'lr': 1e-3}, 
    model_name='Air_RNN',
    log_tensorboard=True,
    random_state=42
)

my_model.fit(train_transformed, val_series=val_transformed, verbose=True)

def eval_model(model):
    pred_series = model.predict(n=26)

    plt.figure(figsize=(8,5))
    series_transformed.plot(label='actual')
    pred_series.plot(label='forecast')
    plt.title('MAPE: {:.2f}%'.format(mape(pred_series, val_transformed)))
    plt.legend()
    plt.show()
    
eval_model(my_model)


### Visualize Forecast 
#######################################################

# sns.set_theme()

# plt.figure(figsize=(10,5))
# plt.suptitle("Time Series Forecast", fontsize=20)
# series.plot(label='actual')
# prediction.plot(label='forecast', lw=3)
# plt.legend()
# plt.show()
'''