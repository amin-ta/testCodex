# MLOps System Example

This repository provides a small demonstration of how an MLOps service might
handle image datasets and training jobs. It uses **Flask** for the API layer and
**ultralytics** for YOLO model training.

## Structure

- `mlops_system/` contains the application modules:
 - `app.py` – Flask server exposing dataset and training endpoints and serving a small web UI.
  - `dataset.py` – utilities for uploading, listing and merging datasets.
  - `training.py` – wrapper that launches YOLO training.
  - `auth.py` – very simple token based authentication helper.

Datasets are stored under the `datasets/` directory created at runtime.

## Usage

Install the required packages and run the server. The root page `/` provides a simple browser UI for uploading datasets and starting training jobs:


```bash
pip install flask ultralytics
python -m mlops_system.app
```

The API accepts an `Authorization` header matching a token from `mlops_system.auth.USERS`.

Example endpoints:

- `POST /upload` – form-data with `file` (zip) and `name` parameters.
- `GET /datasets` – list available datasets.
- `POST /datasets/merge` – JSON body `{ "names": [..], "format": "zip" }`.
- `POST /datasets/<name>/train` – JSON body `{ "val_split": 0.2 }` to start YOLO training.

You can also use the web interface at `/` instead of calling the endpoints manually.

This project is a minimal skeleton and does not implement advanced features such
as user permissions, searching by object labels or a production-ready auth
system. It can be extended to meet specific company requirements.

## Regression Trader (MQL5)

A simple expert advisor for MetaTrader 5 is provided under `mql5/RegressionTrader.mq5`. It uses polynomial regression across multiple timeframes and a moving average filter to generate buy or sell signals. Key parameters such as the list of timeframes, regression degree, number of bars analyzed and moving average period can be adjusted via input settings in MetaTrader.

To use the expert advisor:

1. Copy `RegressionTrader.mq5` to your MetaTrader `Experts` directory.
2. Compile the file in MetaEditor.
3. Attach the EA to a gold chart and configure the inputs to suit your trading preferences.

This code is a basic template and may require further tuning before live trading.

