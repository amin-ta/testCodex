import os
from typing import Optional

from ultralytics import YOLO

from mlops_system.dataset import DATASET_DIR


def train_yolo(dataset_name: str, val_split: float = 0.2, model: str = "yolov8n.pt", epochs: int = 10) -> str:
    """Train a YOLO model on a given dataset."""
    dataset_path = os.path.join(DATASET_DIR, dataset_name)
    if not os.path.isdir(dataset_path):
        raise FileNotFoundError(f"Dataset {dataset_name} not found")

    # Assuming dataset follows YOLO directory structure with 'images' and 'labels'
    data_yaml = os.path.join(dataset_path, "data.yaml")
    if not os.path.exists(data_yaml):
        raise FileNotFoundError("data.yaml describing the dataset is required")

    model = YOLO(model)
    results = model.train(data=data_yaml, epochs=epochs, val=val_split)
    return results.save_dir
