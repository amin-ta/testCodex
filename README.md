# MLOps System Example

This repository provides a small demonstration of how an MLOps service might
handle image datasets and training jobs. It uses **Flask** for the API layer and
**ultralytics** for YOLO model training.

## Structure

- `mlops_system/` contains the application modules:
  - `app.py` – Flask server exposing dataset and training endpoints.
  - `dataset.py` – utilities for uploading, listing and merging datasets.
  - `training.py` – wrapper that launches YOLO training.
  - `auth.py` – very simple token based authentication helper.

Datasets are stored under the `datasets/` directory created at runtime.

## Usage

Install the required packages and run the server:

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

This project is a minimal skeleton and does not implement advanced features such
as user permissions, searching by object labels or a production-ready auth
system. It can be extended to meet specific company requirements.
