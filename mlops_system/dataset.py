import os
import zipfile
import tarfile
from typing import List

DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', 'datasets')
os.makedirs(DATASET_DIR, exist_ok=True)

def _unpack_zip(zip_path: str, dest: str) -> None:
    """Unpack a zip file to destination."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(dest)

def upload_dataset(zip_path: str, name: str) -> str:
    """Upload a dataset by unzipping to datasets folder."""
    dataset_path = os.path.join(DATASET_DIR, name)
    os.makedirs(dataset_path, exist_ok=True)
    _unpack_zip(zip_path, dataset_path)
    return dataset_path

def list_datasets() -> List[str]:
    return [
        d
        for d in os.listdir(DATASET_DIR)
        if os.path.isdir(os.path.join(DATASET_DIR, d))
    ]

def merge_datasets(names: List[str], output_path: str, fmt: str = 'zip') -> str:
    tmp_dir = os.path.join(DATASET_DIR, '_merge_temp')
    os.makedirs(tmp_dir, exist_ok=True)
    for name in names:
        src = os.path.join(DATASET_DIR, name)
        if not os.path.isdir(src):
            continue
        for root, _, files in os.walk(src):
            rel = os.path.relpath(root, src)
            dest_root = os.path.join(tmp_dir, rel)
            os.makedirs(dest_root, exist_ok=True)
            for f in files:
                dest_file = os.path.join(dest_root, f)
                if not os.path.exists(dest_file):
                    os.link(os.path.join(root, f), dest_file)
    if fmt == 'zip':
        with zipfile.ZipFile(output_path, 'w') as zf:
            for root, _, files in os.walk(tmp_dir):
                for f in files:
                    full = os.path.join(root, f)
                    arc = os.path.relpath(full, tmp_dir)
                    zf.write(full, arc)
    else:
        with tarfile.open(output_path, 'w') as tf:
            for root, _, files in os.walk(tmp_dir):
                for f in files:
                    full = os.path.join(root, f)
                    arc = os.path.relpath(full, tmp_dir)
                    tf.add(full, arc)
    return output_path
